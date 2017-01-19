FROM golang:1.6

RUN apt-get update -y && apt-get install -y python-pip && pip install envtpl

# Add codis
Add . /go/src/github.com/CodisLabs/codis/
WORKDIR /go/src/github.com/CodisLabs/codis/

RUN export GO15VENDOREXPERIMENT=0 && go get github.com/tools/godep && export GOPATH=`godep path`:$GOPATH && godep restore && make clean && make && make gotest
