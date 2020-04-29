import pytest


@pytest.fixture(scope='session')
def collection_name():
    return 'schema_test'


@pytest.fixture()
def object_attributes(collection_name):
    from tests.utilities.common import delete_test_collections, get_schema_example
    delete_test_collections()
    example = get_schema_example()
    return {k: v for k, v in example.items() if k not in {'created', 'active', 'updated', 'id'}}
