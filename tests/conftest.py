import pytest


@pytest.fixture(scope='session', )
def test_directory():
    import os
    return os.path.abspath(__file__).replace('conftest.py', '')


@pytest.fixture(scope='session', )
def app_settings(test_directory):
    from framework.core.settings import get_app_settings
    import os
    return get_app_settings(env_folder=os.path.join(test_directory, 'mocks/settings'))
