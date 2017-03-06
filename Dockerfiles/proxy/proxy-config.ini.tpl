##### Properties below are for dashboard and proxies
coordinator={{ CODIS_COORDINATOR | default("zookeeper") }}
zk={{ CODIS_ZK }}
product={{ CODIS_PRODUCT }}

#####
password={{ CODIS_PASSWORD | default("") }}

##### Properties below are only for proxies
backend_ping_period={{ CODIS_BACKEND_PING_PERIOD | default("5") }}
session_max_timeout={{ CODIS_SESSION_MAX_TIMEOUT | default("1200") }}
session_max_bufsize={{ CODIS_SESSION_MAX_BUFSIZE | default("131072") }}
session_max_pipeline={{ CODIS_SESSION_MAX_PIPELINE | default("1024") }}
zk_session_timeout={{ CODIS_ZK_SESSION_TIMEOUT | default("20000") }}

##### must be different for each proxy
proxy_id={{ CODIS_PROXY_ID }}
