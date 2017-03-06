#!/bin/bash

set -e
python /go/src/github.com/CodisLabs/codis/Dockerfiles/dashboard/dashboard_env_check.py
envtpl -o /opt/codis/dashboard-config.ini --keep-template /go/src/github.com/CodisLabs/codis/Dockerfiles/dashboard/dashboard-config.ini.tpl
#for ((i=0;i<10;++i)); do /opt/codis/bin/codis-config -c /opt/codis/dashboard-config.ini slot init 2>&1 | tee /opt/codis/slot_init.log; grep 'slots already initialized' /opt/codis/slot_init.log; if [ $? -eq 0 ]; then echo "$i: already" >>/opt/codis/slot_init_result.log; break; fi; grep '"msg": "OK"' /opt/codis/slot_init.log; if [ $? -eq 0 ]; then echo "$i: ok" >>/opt/codis/slot_init_result.log; break; fi; echo "$i: failed" >>/opt/codis/slot_init_result.log; done &
/opt/codis/bin/codis-config -c /opt/codis/dashboard-config.ini dashboard --addr=:$CODIS_DASHBOARD_PORT $CODIS_DASHBOARD_ARGS
