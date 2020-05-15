import pytest


@pytest.mark.parametrize("collection_name,full_collection_name_flag",
                         [('collection_name', False), ('full_collection_name', True)])
def test_update_single_record(object_attributes, collection_name, full_collection_name_flag, get_test_collections):
    from stratus_api.core.common import generate_random_id
    from stratus_api.document import update_object, create_object
    from tests.document.conftest import delete_collection_documents
    from stratus_api.document.utilities import generate_collection_firestore_name

    collection_name = get_test_collections[collection_name][0]
    generate_collection_name = generate_collection_firestore_name(collection_name=collection_name,
                                                                  full_collection_name=full_collection_name_flag)
    assert len(generate_collection_name.split('-')) == 3
    object_attributes = {k: v for k, v in object_attributes.items() if k not in ['id']}
    object_attributes['sub_object'] = dict(object_1=generate_random_id(), object_2=generate_random_id())
    obj = create_object(collection_name=collection_name, unique_keys=['name'], attributes=object_attributes,
                        full_collection_name=full_collection_name_flag)
    assert len(obj['sub_object'].keys()) == 2
    update_attributes = dict(sub_object=dict(attributes_3='New attributes'))
    updated_obj = update_object(collection_name=collection_name, full_collection_name=full_collection_name_flag,
                                object_id=obj['id'], attributes=update_attributes)
    assert len(updated_obj['sub_object'].keys()) == 3
    delete_collection_documents(collection=collection_name)
    delete_collection_documents(collection=collection_name)


def test_update_single_record_override(object_attributes, collection_name):
    from stratus_api.core.common import generate_random_id
    from stratus_api.document import update_object, create_object
    from tests.document.conftest import delete_collection_documents
    object_attributes = {k: v for k, v in object_attributes.items() if k not in ['id']}
    object_attributes['sub_object'] = dict(object_1=generate_random_id(), object_2=generate_random_id())
    obj = create_object(collection_name=collection_name, unique_keys=['name'], attributes=object_attributes)
    assert len(obj['sub_object'].keys()) == 2
    update_attributes = dict(sub_object=dict(attributes_3='New attributes'))
    updated_obj = update_object(collection_name=collection_name, object_id=obj['id'], attributes=update_attributes,
                                override=True)
    assert len(updated_obj['sub_object'].keys()) == 1
    delete_collection_documents(collection=collection_name)
    delete_collection_documents(collection=collection_name)



def test_update_batch():
    from stratus_api.document import update_object


def test_update_custom_message_handling():
    pass
