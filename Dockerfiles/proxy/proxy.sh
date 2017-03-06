#!/bin/bash

set -e
python /go/src/github.com/CodisLabs/codis/Dockerfiles/proxy/proxy_env_check.py
envtpl -o /opt/codis/proxy-config.ini --keep-template /go/src/github.com/CodisLabs/codis/Dockerfiles/proxy/proxy-config.ini.tpl
if [[ $ALLOW_METRICS_COLLECTION == "1" ]]; then
    envtpl -o /etc/collectd/collectd.conf --keep-template /go/src/github.com/CodisLabs/codis/Dockerfiles/collectd/codis_proxy_collectd.conf.tpl
    service collectd start
fi
python /go/src/github.com/CodisLabs/codis/Dockerfiles/logrotate/crontab_generator.py
service cron start
/opt/codis/bin/codis-proxy -c /opt/codis/proxy-config.ini --addr=$CODIS_PROXY_HOST:$CODIS_PROXY_PORT --http-addr=$CODIS_PROXY_HOST:$CODIS_PROXY_HTTP_PORT $CODIS_PROXY_ARGS
