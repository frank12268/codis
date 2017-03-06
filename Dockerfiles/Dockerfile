FROM golang:1.6

# https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/
RUN apt-get update -y && apt-get install -y python-dev python-pip collectd cron logrotate && pip install envtpl && rm -rf /var/lib/apt/lists/*

# Add codis
Add . /go/src/github.com/CodisLabs/codis/
WORKDIR /go/src/github.com/CodisLabs/codis/

# Donwload dependencies, compile and test
RUN export GO15VENDOREXPERIMENT=0 && go get github.com/tools/godep && export GOPATH=`godep path`:$GOPATH && godep restore && make clean && make && make gotest

# Setup environment
RUN mkdir -p /opt/codis/log; ln -s /go/src/github.com/CodisLabs/codis/bin /opt/codis/bin; mkdir -p /opt/codis/collectd; ln -s /go/src/github.com/CodisLabs/codis/Dockerfiles/collectd/redis_info.py /opt/codis/collectd/redis_info.py; ln -s /go/src/github.com/CodisLabs/codis/Dockerfiles/collectd/codis_proxy.py /opt/codis/collectd/codis_proxy.py; ln -s /go/src/github.com/CodisLabs/codis/Dockerfiles/dashboard/dashboard.sh /opt/codis/dashboard.sh; ln -s /go/src/github.com/CodisLabs/codis/Dockerfiles/server/server.sh /opt/codis/server.sh; ln -s /go/src/github.com/CodisLabs/codis/Dockerfiles/proxy/proxy.sh /opt/codis/proxy.sh; cp /go/src/github.com/CodisLabs/codis/Dockerfiles/logrotate/codis_logrotate /etc/logrotate.d/codis

VOLUME /opt/codis/data

WORKDIR /opt/codis
