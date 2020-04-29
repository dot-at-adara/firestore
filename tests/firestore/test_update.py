import pytest


def test_update_single_record(object_attributes, collection_name):
    from framework.firestore import update_object, create_object, get_objects
    object_attributes = {k: v for k, v in object_attributes.items() if k not in ['id']}
    obj = create_object(collection_name=collection_name, unique_keys=['name'], attributes=object_attributes,
                        publish=True)
    assert len(obj['sub_object'].keys()) == 2
    update_attributes = dict(sub_object=dict(attributes_3='New attributes'))
    updated_obj = update_object(collection_name=collection_name, object_id=obj['id'], attributes=update_attributes)
    assert len(updated_obj['sub_object'].keys()) == 3


def test_update_single_record_override(object_attributes, collection_name):
    from framework.firestore import update_object, create_object, get_objects
    object_attributes = {k: v for k, v in object_attributes.items() if k not in ['id']}
    obj = create_object(collection_name=collection_name, unique_keys=['name'], attributes=object_attributes,
                        publish=True)
    assert len(obj['sub_object'].keys()) == 2
    update_attributes = dict(sub_object=dict(attributes_3='New attributes'))
    updated_obj = update_object(collection_name=collection_name, object_id=obj['id'], attributes=update_attributes,
                                override=True)
    assert len(updated_obj['sub_object'].keys()) == 1


def test_update_batch():
    from framework.firestore import update_object


def test_update_custom_message_handling():
    pass
