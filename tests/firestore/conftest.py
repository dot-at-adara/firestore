import pytest


@pytest.fixture(scope='session')
def collection_name():
    return 'test'


@pytest.fixture()
def object_attributes(collection_name):
    delete_collection_documents(collection=collection_name)
    example = {
        "id": "bd5ac04c-32dc-4705-885d-81ae160079a7",
        "name": "example_name",
        "active": True,
        "example_field": "example_name"
    }
    return {k: v for k, v in example.items() if k not in {'created', 'active', 'updated', 'id'}}


def delete_collection_documents(collection):
    from framework.firestore import create_db_client
    db = create_db_client()
    chunk_size = 10
    while chunk_size > 0:
        chunk_size = 0
        chunk = db.collection(collection).limit(100).get()
        for document in chunk:
            document.reference.delete()
            chunk_size += 1
    pass
