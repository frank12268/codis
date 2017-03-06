#!/bin/bash

set -e
python /go/src/github.com/CodisLabs/codis/Dockerfiles/server/server_env_check.py
if [[ $ALLOW_METRICS_COLLECTION == "1" ]]; then
    envtpl -o /etc/collectd/collectd.conf --keep-template /go/src/github.com/CodisLabs/codis/Dockerfiles/collectd/redis_info_collectd.conf.tpl
    service collectd start
fi
python /go/src/github.com/CodisLabs/codis/Dockerfiles/logrotate/crontab_generator.py
service cron start
/opt/codis/bin/codis-server /go/src/github.com/CodisLabs/codis/Dockerfiles/server/redis.conf --port $CODIS_SERVER_PORT --maxmemory $CODIS_SERVER_MAX_MEMORY $CODIS_SERVER_ARGS
