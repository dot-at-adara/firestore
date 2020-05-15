import pytest


def test_single_object_flow(object_attributes, collection_name):
    from stratus_api.core.settings import get_app_settings
    from stratus_api.document import create_object, get_objects, update_object, delete_object
    from tests.document.conftest import delete_collection_documents

    app_settings = get_app_settings()
    obj = create_object(collection_name=collection_name, unique_keys=['name'], attributes=object_attributes)
    assert isinstance(obj, dict)
    assert isinstance(obj.get('id'), str)
    with pytest.raises(ValueError):
        create_object(collection_name=collection_name, unique_keys=['name'], attributes=object_attributes)
    assert obj['active']
    objects = get_objects(collection_name=collection_name, eq_id=obj['id'])
    assert isinstance(objects, list)
    assert len(objects) == 1
    new_name = 'New Name'
    obj['name'] = new_name
    updated_object = update_object(collection_name=collection_name, object_id=obj['id'], attributes=obj)
    assert updated_object['created'] < updated_object['updated']

    old_objects = get_objects(collection_name=collection_name, eq_id=obj['id'], eq_name=obj['name'])
    assert len(old_objects)

    new_objects = get_objects(collection_name=collection_name, eq_id=obj['id'], eq_name=new_name)
    assert len(new_objects) == 1

    delete_object(collection_name=collection_name, object_id=obj['id'])
    deleted_objects = get_objects(collection_name=collection_name, eq_id=obj['id'], eq_name=new_name)
    assert len(deleted_objects) == 0
    inactive_objects = get_objects(collection_name=collection_name, eq_id=obj['id'], eq_name=new_name, active=False)
    assert len(inactive_objects) == 1
    delete_collection_documents(collection=collection_name)
    delete_collection_documents(collection=collection_name)

