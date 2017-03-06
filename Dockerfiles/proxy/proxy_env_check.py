import os

MUST_HAVE_ENVIRONMENTS = [
    'CODIS_GROUP_NAME',
    'CODIS_COMPONENT_TYPE',
    'CODIS_ZK',
    'CODIS_PRODUCT',
    'ALLOW_METRICS_COLLECTION',
    'CODIS_PROXY_ID',
    'CODIS_PROXY_HOST',
    'CODIS_PROXY_PORT',
    'CODIS_PROXY_HTTP_PORT',
    'CODIS_PROXY_HOST_HOST',
    'CODIS_PROXY_HOST_PORT',
    'CODIS_PROXY_HOST_HTTP_PORT',
]

MUST_HAVE_METRICS_ENVIRONMENTS = [
    'COLLECTD_HOST',
    'GRAPHITE_PREFIX',
]

if __name__ == '__main__':
    for env_key in MUST_HAVE_ENVIRONMENTS:
        assert os.environ.get(env_key) is not None, 'OS ENV KEY %s not existed' % (env_key)
    port = int(os.environ.get('CODIS_PROXY_PORT'))
    http_port = int(os.environ.get('CODIS_PROXY_HTTP_PORT'))
    host_port = int(os.environ.get('CODIS_PROXY_HOST_PORT'))
    host_http_port = int(os.environ.get('CODIS_PROXY_HOST_HTTP_PORT'))
    assert os.environ.get('CODIS_COMPONENT_TYPE').lower() == 'proxy', os.environ.get('CODIS_COMPONENT_TYPE')
    if os.environ.get('ALLOW_METRICS_COLLECTION') == '1':
        for env_key in MUST_HAVE_METRICS_ENVIRONMENTS:
            assert os.environ.get(env_key) is not None, 'OS ENV KEY %s not existed' % (env_key)
