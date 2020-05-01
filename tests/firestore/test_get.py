import pytest
from google.api_core.exceptions import FailedPrecondition


@pytest.fixture()
def setup_objects(collection_name, object_attributes):
    from framework.firestore import create_object, create_db_client
    from tests.firestore.conftest import delete_collection_documents
    delete_collection_documents(collection=collection_name)
    delete_collection_documents(collection=collection_name)
    obj = object_attributes
    batch = create_db_client().batch()
    objects = list()
    for i in range(20):
        obj['name'] = str(i)
        if i >= 10:
            obj['filter_1'] = 'high'
        else:
            obj['filter_1'] = 'low'
        if i % 2:
            obj['filter_2'] = 'yes'
        else:
            obj['filter_2'] = 'no'
        o, batch = create_object(collection_name=collection_name, unique_keys=['name'], attributes=obj,
                                 hash_id=True, batch=batch)
        objects.append(o)
    batch.commit()
    return objects


def test_get_object_no_filter_sorts_id_ascending(setup_objects, collection_name):
    from framework.firestore import get_objects

    objects = get_objects(collection_name=collection_name, sort_keys=['id_ascending'], active=False, limit=None)
    current_id = '0'
    assert len(objects) == 20
    for o in objects:
        assert o['id'] > current_id
        current_id = o['id']


def test_get_object_1_filter_no_sort(setup_objects, collection_name):
    from framework.firestore import get_objects
    assert len(get_objects(collection_name=collection_name, eq_filter_1='high', limit=None)) == 10


def test_get_object_bad_sort_no_index(setup_objects, collection_name):
    from framework.firestore import get_objects
    with pytest.raises(FailedPrecondition):
        get_objects(collection_name=collection_name, eq_filter_1='high',
                    sort_keys=['id_ascending', 'created_descending'], limit=None)


def test_get_object_multi_filter_sort(setup_objects, collection_name):
    from framework.firestore import get_objects
    get_objects(collection_name=collection_name, eq_filter_1='high',
                sort_keys=['filter_2_ascending', 'name_descending'], limit=None, active=False)


def test_get_object_multi_filter_sort_wrong_order_fails(setup_objects, collection_name):
    from framework.firestore import get_objects
    with pytest.raises(FailedPrecondition):
        get_objects(collection_name=collection_name, eq_filter_1='high',
                    sort_keys=['name_descending', 'filter_2_ascending'], limit=None, active=False)


def test_get_object_partial_index_fails(setup_objects, collection_name):
    from framework.firestore import get_objects
    with pytest.raises(FailedPrecondition):
        get_objects(collection_name=collection_name, eq_filter_1='high', sort_keys=['filter_2_ascending'], limit=None,
                    active=False)


def test_get_object_cursor(setup_objects, collection_name):
    from framework.firestore import get_objects
    objects, cursor_id = get_objects(collection_name=collection_name, active=False, limit=10, create_cursor=True)
    assert len(objects) == 10
    new_objects, cursor_id = get_objects(collection_name=collection_name, active=False, limit=10, create_cursor=True,
                                         cursor_id=cursor_id)
    assert len(new_objects) == 10
    last_objects, cursor_id = get_objects(collection_name=collection_name, active=False, limit=10, create_cursor=True,
                                          cursor_id=cursor_id)

    assert len(last_objects) == 0
    assert cursor_id is None


def test_get_object_without_cursor(setup_objects, collection_name):
    from framework.firestore import get_objects


def test_get_object_cursor_sort(setup_objects, collection_name):
    from framework.firestore import get_objects


def test_get_object_without_cursor_sort(setup_objects, collection_name):
    from framework.firestore import get_objects
