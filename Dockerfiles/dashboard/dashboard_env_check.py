import os

MUST_HAVE_ENVIRONMENTS = [
    'CODIS_GROUP_NAME',
    'CODIS_COMPONENT_TYPE',
    'CODIS_ZK',
    'CODIS_PRODUCT',
    'CODIS_DASHBOARD_PORT',
    'CODIS_DASHBOARD_HOST_HOST',
    'CODIS_DASHBOARD_HOST_PORT',
]

if __name__ == '__main__':
    for env_key in MUST_HAVE_ENVIRONMENTS:
        assert os.environ.get(env_key) is not None, 'OS ENV KEY %s not existed' % (env_key)
    port = int(os.environ.get('CODIS_DASHBOARD_PORT'))
    host_port = int(os.environ.get('CODIS_DASHBOARD_HOST_PORT'))
    assert os.environ.get('CODIS_COMPONENT_TYPE').lower() == 'dashboard', os.environ.get('CODIS_COMPONENT_TYPE')
