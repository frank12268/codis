import os

MUST_HAVE_ENVIRONMENTS = [
    'CODIS_GROUP_NAME',
    'CODIS_COMPONENT_TYPE',
    'CODIS_SENTINEL_PORT',
    'CODIS_SENTINEL_HOST_HOST',
    'CODIS_SENTINEL_HOST_PORT',
]

if __name__ == '__main__':
    for env_key in MUST_HAVE_ENVIRONMENTS:
        assert os.environ.get(env_key) is not None, 'OS ENV KEY %s not existed' % (env_key)
    port = int(os.environ.get('CODIS_SENTINEL_PORT'))
    host_port = int(os.environ.get('CODIS_SENTINEL_HOST_PORT'))
    assert os.environ.get('CODIS_COMPONENT_TYPE').lower() == 'sentinel', os.environ.get('CODIS_COMPONENT_TYPE')
