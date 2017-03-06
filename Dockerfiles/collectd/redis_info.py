#! /usr/bin/python
# ref:
# https://github.com/signalfx/redis-collectd-plugin/blob/master/redis_info.py

import collectd
import functools
import re
import socket

CONFIGS = []
REDIS_INFO = {}


def log_verbose(enabled, plugin_name, msg):
    if not enabled:
        return
    collectd.info('[%s plugin]: %s' % (plugin_name, msg))


def configure_callback(conf):
    d = {
        'host': '127.0.0.1',
        'port': 6379,
        'auth': None,
        'verbose': False,
    }
    log = functools.partial(log_verbose, True, 'redis')
    for node in conf.children:
        key = node.key.lower()
        val = node.values[0]
        log('Analyzing config %s key (value: %s)' % (key, val))
        if key == 'port':
            d[key] = int(val)
        elif key == 'verbose':
            d[key] = bool(val)
        elif key in ['host', 'auth', 'instance']:
            d[key] = val
        else:
            searchObj = re.search(r'redis_(.*)$', key, re.M | re.I)
            if searchObj:
                log('Matching expression found: key: %s - value: %s' % (searchObj.group(1), val))
                global REDIS_INFO
                REDIS_INFO[searchObj.group(1), val] = True
            else:
                collectd.warning('[redis plugin]: Unknown config key: %s.' % (key))
    if 'instance' not in d:
        d['instance'] = '%s_%d' % (d['host'], d['port'])
    d['log'] = functools.partial(log_verbose, d['verbose'], d['instance'])
    CONFIGS.append(d)


def parse_info(info_lines):
    """Parse info response from Redis"""
    info = {}
    for line in info_lines:
        if "" == line or line.startswith('#'):
            continue

        if ':' not in line:
            collectd.warning('redis_info plugin: Bad format for info line: %s' % line)
            continue

        key, val = line.split(':')

        # Handle multi-value keys (for dbs and slaves).
        # db lines look like "db0:keys=10,expire=0"
        # slave lines look like
        # "slave0:ip=192.168.0.181,port=6379,state=online,offset=1650991674247,lag=1"
        if ',' in val:
            split_val = val.split(',')
            for sub_val in split_val:
                k, _, v = sub_val.rpartition('=')
                sub_key = "{0}_{1}".format(key, k)
                info[sub_key] = v
        else:
            info[key] = val

    # compatibility with pre-2.6 redis (used changes_since_last_save)
    info["changes_since_last_save"] = info.get("changes_since_last_save", info.get("rdb_changes_since_last_save"))
    return info


def fetch_info(conf):
    """Connect to Redis server and request info"""
    log = conf['log']
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((conf['host'], conf['port']))
        log('Connected to Redis at %s:%s' % (conf['host'], conf['port']))
    except socket.error, e:
        collectd.error('redis_info plugin: Error connecting to %s:%d - %r' % (conf['host'], conf['port'], e))
        return None

    fp = s.makefile('r')

    if conf['auth'] is not None:
        log('Sending auth command')
        s.sendall('auth %s\r\n' % (conf['auth']))

        status_line = fp.readline()
        if not status_line.startswith('+OK'):
            # -ERR invalid password
            # -ERR Client sent AUTH, but no password is set
            collectd.error('redis_info plugin: Error sending auth to %s:%d - %r' % (conf['host'], conf['port'], status_line))
            return None

    log('Sending info command')
    s.sendall('info\r\n')

    status_line = fp.readline()

    if status_line.startswith('-'):
        collectd.error('redis_info plugin: Error response from %s:%d - %r' % (conf['host'], conf['port'], status_line))
        s.close()
        return None

    # status_line looks like: $<content_length>
    content_length = int(status_line[1:-1])
    data = fp.read(content_length)
    log('Received data: %s' % data)
    s.close()

    linesep = '\r\n' if '\r\n' in data else '\n'
    return parse_info(data.split(linesep))


def dispatch_value(log, info, key, type, plugin_instance=None, type_instance=None):
    """Read a key from info response data and dispatch a value"""
    if key not in info:
        collectd.warning('redis_info plugin: Info key not found: %s' % key)
        return

    if plugin_instance is None:
        plugin_instance = 'unknown redis'
        collectd.error('redis_info plugin: plugin_instance is not set, Info key: %s' % key)

    if not type_instance:
        type_instance = key

    try:
        value = int(info[key])
    except ValueError:
        value = float(info[key])

    log('Sending value: %s=%s' % (type_instance, value))

    val = collectd.Values(plugin='redis_info')
    val.type = type
    val.type_instance = type_instance
    val.plugin_instance = plugin_instance
    val.values = [value]
    # https://github.com/collectd/collectd/issues/716
    val.meta = {'0': True}
    val.dispatch()


def read_callback():
    for conf in CONFIGS:
        plugin_instance = conf['instance']
        log = conf['log']
        info = fetch_info(conf)
        if info is None:
            collectd.error('[%s plugin]: redis info command failure' % (plugin_instance))
            continue
        for kvtuple, _t in REDIS_INFO.iteritems():
            key, val = kvtuple
            if key == 'total_connections_received' and val == 'counter':
                dispatch_value(log, info, 'total_connections_received', 'counter', plugin_instance, 'connections_received')
            elif key == 'total_commands_processed' and val == 'counter':
                dispatch_value(log, info, 'total_commands_processed', 'counter', plugin_instance, 'commands_processed')
            else:
                dispatch_value(log, info, key, val, plugin_instance)

collectd.register_config(configure_callback)
collectd.register_read(read_callback)
