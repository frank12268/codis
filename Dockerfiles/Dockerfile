FROM golang:1.7.3

RUN apt-get update -y; apt-get install -y autoconf python-dev python-pip collectd && pip install envtpl

ENV GOPATH /gopath
COPY . /gopath/src/github.com/CodisLabs/codis

RUN make -C /gopath/src/github.com/CodisLabs/codis distclean && make -C /gopath/src/github.com/CodisLabs/codis build-all

RUN mkdir -p /opt/codis/log; mkdir -p /opt/codis/collectd; ln -s /gopath/src/github.com/CodisLabs/codis/Dockerfiles/collectd/redis_info.py /opt/codis/collectd/redis_info.py; ln -s /gopath/src/github.com/CodisLabs/codis/Dockerfiles/collectd/codis_proxy_3_1.py /opt/codis/collectd/codis_proxy.py; ln -s /gopath/src/github.com/CodisLabs/codis/Dockerfiles/dashboard/dashboard.sh /opt/codis/dashboard.sh; ln -s /gopath/src/github.com/CodisLabs/codis/Dockerfiles/server/server.sh /opt/codis/server.sh; ln -s /gopath/src/github.com/CodisLabs/codis/Dockerfiles/proxy/proxy.sh /opt/codis/proxy.sh; ln -s /gopath/src/github.com/CodisLabs/codis/Dockerfiles/sentinel/sentinel.sh /opt/codis/sentinel.sh

VOLUME /opt/codis/data
WORKDIR /opt/codis
