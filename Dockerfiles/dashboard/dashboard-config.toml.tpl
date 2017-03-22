# Set Coordinator, only accept "zookeeper" & "etcd" & "filesystem".
coordinator_name = "{{ CODIS_COORDINATOR_NAME | default("zookeeper") }}"
coordinator_addr = "{{ CODIS_ZK }}"

# Set Codis Product Name/Auth.
product_name = "{{ CODIS_PRODUCT }}"
product_auth = "{{ CODIS_PASSWORD | default("") }}"

# Set bind address for admin(rpc), tcp only.
admin_addr = "{{ CODIS_DASHBOARD_HOST | default("0.0.0.0") }}:{{ CODIS_DASHBOARD_PORT }}"

# Set configs for redis sentinel.
sentinel_quorum = {{ CODIS_SENTINEL_QUORUM }}
sentinel_parallel_syncs = {{ CODIS_SENTINEL_PARALLEL_SYNCS | default(1) }}
sentinel_down_after = "{{ CODIS_SENTINEL_DOWN_AFTER | default("30s") }}"
sentinel_failover_timeout = "{{ CODIS_SENTINEL_FAILOVER_TIMEOUT | default("10m") }}"
sentinel_notification_script = "{{ CODIS_SENTINEL_NOTIFICATION_SCRIPT | default("") }}"
sentinel_client_reconfig_script = "{{ CODIS_SENTINEL_CLIENT_RECONFIG_SCRIPT | default("") }}"
