Hostname "{{ COLLECTD_HOST }}"
FQDNLookup false
ReadThreads 5
WriteThreads 5
Interval 5
Timeout 2

#LoadPlugin "logfile"
#<Plugin "logfile">
#    LogLevel "info"
#    File "/opt/codis/log/collectd-proxy.log"
#    Timestamp true
#</Plugin>

LoadPlugin write_graphite
<Plugin "write_graphite">
    <Carbon>
        Host "{{ GRAPHITE_HOST | default("els.relay.devops-graphite.prod.hulu.com") }}"
        Port {{ GRAPHITE_PORT | default("2013") }}
        Protocol "{{ GRAPHITE_PROTOCOL | default("udp") }}"
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
