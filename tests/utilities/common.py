def delete_test_collections():
    # from server import collections, app_settings

    assert 'test' in app_settings['environment'].lower()
    for collection_name, collection in collections.items():
        delete_collection_documents(collection=collection)
    return True


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


def generate_random_id():
    """Generate a random id

    :return: a unique UUID4 formatted string
    """
    import uuid
    return str(uuid.uuid4())


def generate_hash_id(data):
    import json
    import uuid
    import hashlib
    hash_id = uuid.UUID(hashlib.md5(str(json.dumps(data, sort_keys=True)).encode('utf-8')).hexdigest())
    return str(hash_id)


def get_schema_example():
    return {
        "type": "object",
        "properties":
            {
                "id": {
                    "type": "string",
                    "example": "bd5ac04c-32dc-4705-885d-81ae160079a7"
                },
                "active": {
                    "type":"boolean",
                    "example":True
                },
                "example_field":{
                    "type":"string",
                    "example":"example_field"
                }
            },
        "additionalProperties": False
    }
