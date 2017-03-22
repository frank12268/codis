dir /opt/codis/data
protected-mode no
save ""
slave-announce-ip {{ CODIS_SERVER_HOST_HOST }}
slave-announce-port {{ CODIS_SERVER_HOST_PORT }}