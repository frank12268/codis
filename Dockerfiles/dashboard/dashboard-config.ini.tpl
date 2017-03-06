##### Properties below are for dashboard and proxies
coordinator={{ CODIS_COORDINATOR | default("zookeeper") }}
zk={{ CODIS_ZK }}
product={{ CODIS_PRODUCT }}

#####
dashboard_addr={{ CODIS_DASHBOARD_HOST_HOST }}:{{ CODIS_DASHBOARD_HOST_PORT }}
password={{ CODIS_PASSWORD | default("") }}
