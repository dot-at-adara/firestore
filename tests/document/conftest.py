import pytest


@pytest.fixture(scope='session')
def collection_name(app_settings):
    return 'test'


@pytest.fixture(scope='session')
def full_collection_name(app_settings):
    return "{0}-{1}-{2}{3}".format(app_settings['service_name'], app_settings['environment'], app_settings['prefix'],
                                   'test')


@pytest.fixture()
def get_test_collections(collection_name, full_collection_name):
    return dict(
        collection_name=(collection_name, False),
        full_collection_name=(full_collection_name, True)
    )


@pytest.fixture()
def object_attributes(collection_name):
    from stratus_api.core.common import generate_random_id
    delete_collection_documents(collection=collection_name)
    example = {
        "id": "bd5ac04c-32dc-4705-885d-81ae160079a7",
        "name": generate_random_id(),
        "active": True,
        "example_field": generate_random_id()
    }
    return {k: v for k, v in example.items() if k not in {'created', 'active', 'updated', 'id'}}


def delete_collection_documents(collection):
    from stratus_api.document import create_db_client
    db = create_db_client()
    chunk_size = 10
    from stratus_api.document.utilities import generate_collection_firestore_name
    collection = generate_collection_firestore_name(collection_name=collection)
    while chunk_size > 0:
        chunk_size = 0
        chunk = db.collection(collection).limit(100).get()
        for document in chunk:
            document.reference.delete()
            chunk_size += 1
    pass
