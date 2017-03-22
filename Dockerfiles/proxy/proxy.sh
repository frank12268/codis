#!/bin/bash

set -e
python /gopath/src/github.com/CodisLabs/codis/Dockerfiles/proxy/proxy_env_check.py
envtpl -o /opt/codis/proxy-config.toml --keep-template /gopath/src/github.com/CodisLabs/codis/Dockerfiles/proxy/proxy-config.toml.tpl
if [[ $ALLOW_METRICS_COLLECTION == "1" ]]; then
	envtpl -o /etc/collectd/collectd.conf --keep-template /gopath/src/github.com/CodisLabs/codis/Dockerfiles/collectd/codis_proxy_collectd.conf.tpl
	service collectd start
fi
/gopath/src/github.com/CodisLabs/codis/bin/codis-proxy -c /opt/codis/proxy-config.toml --host-admin=$CODIS_PROXY_HOST_HOST:$CODIS_PROXY_HOST_HTTP_PORT --host-proxy=$CODIS_PROXY_HOST_HOST:$CODIS_PROXY_HOST_PORT --zookeeper=$CODIS_ZK $CODIS_PROXY_ARGS
