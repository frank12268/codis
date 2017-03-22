import os

MUST_HAVE_ENVIRONMENTS = [
    'CODIS_GROUP_NAME',
    'CODIS_COMPONENT_TYPE',
    'ALLOW_METRICS_COLLECTION',
    'CODIS_SERVER_PORT',
    'CODIS_SERVER_HOST_HOST',
    'CODIS_SERVER_HOST_PORT',
    'CODIS_SERVER_MAX_MEMORY',
]

MUST_HAVE_METRICS_ENVIRONMENTS = [
    'COLLECTD_HOST',
    'GRAPHITE_PREFIX',
]

if __name__ == '__main__':
    for env_key in MUST_HAVE_ENVIRONMENTS:
        assert os.environ.get(env_key) is not None, 'OS ENV KEY %s not existed' % (env_key)
    port = int(os.environ.get('CODIS_SERVER_PORT'))
    host_port = int(os.environ.get('CODIS_SERVER_HOST_PORT'))
    assert os.environ.get('CODIS_COMPONENT_TYPE').lower() == 'server', os.environ.get('CODIS_COMPONENT_TYPE')
    if os.environ.get('ALLOW_METRICS_COLLECTION') == '1':
        for env_key in MUST_HAVE_METRICS_ENVIRONMENTS:
            assert os.environ.get(env_key) is not None, 'OS ENV KEY %s not existed' % (env_key)
