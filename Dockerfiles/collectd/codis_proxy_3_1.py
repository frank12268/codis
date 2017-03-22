#! /usr/bin/python

import collectd
import functools
import requests


CONFIGS = []
REDIS_INFO = {}

old_data = {}


def log_verbose(enabled, plugin_instance, msg):
    if not enabled:
        return
    collectd.info('[%s plugin]: %s' % (plugin_instance, msg))


def configure_callback(conf):
    d = {
        'host': '127.0.0.1',
        'port': 6379,
        'verbose': False,
    }
    for node in conf.children:
        key = node.key.lower()
        if key == 'port':
            d[key] = int(node.values[0])
        elif key == 'verbose':
            d[key] = bool(node.values[0])
        elif key in ['host', 'instance']:
            d[key] = node.values[0]
        else:
            collectd.warning('[%s plugin]: Unknown config key/value: %s/%s.' % ('NOT_SET', node.key, node.values[0]))
    if 'instance' not in d:
        d['instance'] = '%s_%s' % (d['host'], d['port'])
    log_verbose(True, 'NOT_SET', 'configured with host = %(host)s, port = %(port)s, verbose = %(verbose)s, instance = %(instance)s' % (d))
    d['log'] = functools.partial(log_verbose, d['verbose'], d['instance'])
    CONFIGS.append(d)


def dispatch_stat(key_type, key, value, plugin_instance, log):
    """Read a key from info response data and dispatch a value"""
    if value is None:
        log('Value not found for %s' % (key))
        return
    log('Sending value[%s]: %s=%s' % (key_type, key, value))

    val = collectd.Values(plugin='codis_proxy')
    val.type = key_type
    val.type_instance = key
    val.values = [value]
    val.plugin_instance = plugin_instance
    # https://github.com/collectd/collectd/issues/716
    val.meta = {'0': True}
    val.dispatch()


def read_callback():
    global old_data
    for conf in CONFIGS:
        try:
            old_dict = old_data.get((conf['host'], conf['port']), {})
            plugin_instance = conf['instance']
            log = conf['log']
            url = 'http://%s:%d/proxy' % (conf['host'], conf['port'])
            data = requests.get(url).json()
            for x in data['stats']['ops']['cmd']:
                if not x['opstr'].endswith(':'):
                    dispatch_stat('counter', 'stats_ops_calls_%s' % (x['opstr']), x['calls'], conf['instance'], log)
                    dispatch_stat('counter', 'stats_ops_usecs_%s' % (x['opstr']), x['usecs'], conf['instance'], log)
                    dispatch_stat('counter', 'stats_ops_fails_%s' % (x['opstr']), x['fails'], conf['instance'], log)
                    tmp = old_dict.get(x['opstr'])
                    if (tmp is not None) and (tmp != (x['calls'], x['usecs'])):
                        dispatch_stat('gauge', 'stats_ops_instant_usecs_%s' % (x['opstr']), (tmp[1] - x['usecs']) / (tmp[0] - x['calls']), conf['instance'], log)
                    old_dict[x['opstr']] = (x['calls'], x['usecs'])
            dispatch_stat('counter', 'stats_ops_total', data['stats']['ops']['total'], conf['instance'], log)
            dispatch_stat('counter', 'stats_ops_fails', data['stats']['ops']['fails'], conf['instance'], log)
            dispatch_stat('gauge', 'stats_ops_qps', data['stats']['ops']['qps'], conf['instance'], log)
            old_data[(conf['host'], conf['port'])] = old_dict
        except Exception as e:
            collectd.error('[%s plugin]: Error collect_metrics from %s:%d - %r' % (conf['instance'], conf['host'], conf['port'], e))


collectd.register_config(configure_callback)
collectd.register_read(read_callback)
