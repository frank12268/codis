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
    Import "codis_proxy"
    <Module "codis_proxy">
        Host "{{ CODIS_PROXY_HOST_HOST }}"
        Port {{ CODIS_PROXY_HOST_HTTP_PORT }}
        Verbose false
        #Verbose true
    </Module>
</Plugin>
