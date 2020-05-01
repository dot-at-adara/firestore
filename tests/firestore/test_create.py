import pytest


def test_create_object_existing_id(object_attributes, collection_name):
    from framework.firestore import create_object, get_objects
    from tests.firestore.conftest import delete_collection_documents
    from framework.core.common import  generate_random_id

    object_attributes['id'] = generate_random_id()
    obj = create_object(collection_name=collection_name, unique_keys=['id'], attributes=object_attributes)
    assert len(object_attributes.keys()) < len(obj.keys())
    assert object_attributes['id'] == obj['id']
    objects = get_objects(collection_name=collection_name, eq_id=object_attributes['id'])
    assert len(objects) == 1
    with pytest.raises(ValueError):
        create_object(collection_name=collection_name, unique_keys=['id'], attributes=object_attributes)
    delete_collection_documents(collection=collection_name)
    delete_collection_documents(collection=collection_name)



def test_create_object_hash_id_overrides_existing_object(object_attributes, collection_name):
    from framework.firestore import create_object
    from framework.core.common import generate_hash_id
    obj = create_object(collection_name=collection_name, unique_keys=['name'], attributes=object_attributes,
                        hash_id=True)
    assert isinstance(obj, dict)
    assert isinstance(obj.get('id'), str)
    assert obj['id'] == generate_hash_id(dict(name=object_attributes['name']))
    new_obj = create_object(collection_name=collection_name, unique_keys=['name'], attributes=object_attributes,
                            hash_id=True)


def test_create_batch_hash_ids(object_attributes, collection_name):
    from framework.firestore import create_object, get_objects
    from framework.firestore import create_db_client
    from copy import deepcopy
    db = create_db_client()
    batch = db.batch()
    for i in range(25):
        obj = deepcopy(object_attributes)
        obj['name'] = str(i)
        obj, batch = create_object(collection_name=collection_name, unique_keys=['name'], attributes=obj,
                                   hash_id=True, batch=batch)
    batch.commit()
    objects, cursor_id = get_objects(collection_name=collection_name, create_cursor=True)
    assert len(objects) == 10
    assert cursor_id is not None
    objects, cursor_id = get_objects(collection_name=collection_name, cursor_id=cursor_id)
    assert len(objects) == 10
    assert cursor_id is not None
    second_set, null_id = get_objects(collection_name=collection_name, cursor_id=cursor_id)
    assert len(second_set) == 5
    assert null_id is None
    objects, null_id = get_objects(collection_name=collection_name, cursor_id=cursor_id)
    assert len(objects) == 0
    assert null_id is None


def test_create_custom_message_handling():
    pass
