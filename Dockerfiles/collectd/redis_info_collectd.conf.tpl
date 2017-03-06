Hostname "{{ COLLECTD_HOST }}"
FQDNLookup false
ReadThreads 5
WriteThreads 5
Interval 5
Timeout 2

LoadPlugin write_graphite
<Plugin "write_graphite">
    <Carbon>
        Host "{{ GRAPHITE_HOST }}"
        Port {{ GRAPHITE_PORT }}
        Protocol "{{ GRAPHITE_PROTOCOL }}"
        Prefix "{{ GRAPHITE_PREFIX }}"
        StoreRates true
        AlwaysAppendDS false
        SeparateInstances true
    </Carbon>
</Plugin>

<LoadPlugin "python">
    Globals true
</LoadPlugin>

<Plugin "python">
    ModulePath "/opt/codis/collectd"
    Import "redis_info"
    <Module "redis_info">
        Host "{{ CODIS_SERVER_HOST_HOST }}"
        Port {{ CODIS_SERVER_HOST_PORT }}
        Verbose false
        #Verbose true

        # Server
        Redis_uptime_in_seconds "gauge"
        # Redis_uptime_in_days "gauge"
        Redis_lru_clock "counter"

        # Clients
        Redis_connected_clients "gauge"
        Redis_blocked_clients "gauge"

        # Memory
        Redis_used_memory "bytes"
        Redis_used_memory_rss "bytes"
        Redis_used_memory_peak "bytes"
        Redis_mem_fragmentation_ratio "gauge"

        # Persistence
        Redis_changes_since_last_save "gauge"
        Redis_rdb_bgsave_in_progress "gauge"

        # Stats
        Redis_total_connections_received "counter"
        Redis_total_commands_processed "counter"
        Redis_instantaneous_ops_per_sec "gauge"
        Redis_total_net_input_bytes "counter"
        Redis_total_net_output_bytes "counter"
        Redis_instantaneous_input_kbps "gauge"
        Redis_instantaneous_output_kbps "gauge"
        Redis_rejected_connections "counter"
        Redis_expired_keys "gauge"
        Redis_evicted_keys "gauge"
        Redis_keyspace_hits "derive"
        Redis_keyspace_misses "derive"
        Redis_pubsub_channels "gauge"
        Redis_pubsub_patterns "gauge"

        # Replication
        Redis_connected_slaves "gauge"
        Redis_master_repl_offset "gauge"
        Redis_master_last_io_seconds_ago "gauge"
        Redis_slave_repl_offset "gauge"

        # CPU

        # Commandstats

        # Cluster

        # Keyspace
    </Module>
</Plugin>
