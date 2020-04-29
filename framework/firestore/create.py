def create_object(collection_name, unique_keys: list, attributes: dict, hash_id=False, batch=None, publish=False,
                  message_formatter=None, user_id=None):
    from handlers.core.common import generate_random_id, generate_hash_id
    from handlers.core.collections import publish_record_update
    from server import collections, collection_schemas
    from handlers.core.firestore.base import create_db_client
    from handlers.core.firestore.get import get_objects

    from datetime import datetime
    from copy import deepcopy
    db = create_db_client()
    now = datetime.utcnow()
    attributes = deepcopy(attributes)
    if 'id' in attributes:
        other_unique_fields = [i for i in unique_keys if i != 'id']
        existing_objects = []
        if other_unique_fields:
            existing_objects += get_objects(
                collection_name=collection_name, active=False,
                **{"eq_{0}".format(i): attributes[i] for i in other_unique_fields}
            )
        existing_objects += get_objects(
            collection_name=collection_name, active=False,
            eq_id=attributes['id']
        )
        if existing_objects:
            raise ValueError("Conflict: object already exists")
        object_id = attributes['id']
    elif hash_id:
        object_id = generate_hash_id(data={i: attributes[i] for i in unique_keys})
    else:
        existing_objects = get_objects(
            collection_name=collection_name, active=True, **{"eq_{0}".format(i): attributes[i] for i in unique_keys}
        )
        if existing_objects:
            raise ValueError("Conflict: object already exists")
        object_id = generate_random_id()
    attributes['id'] = object_id
    attributes['created'] = now
    attributes['updated'] = now
    attributes['active'] = True
    doc_ref = db.collection(collections[collection_name]).document(attributes['id'])

    if batch is not None:
        batch.set(doc_ref, attributes, merge=True)
    else:
        doc_ref.set(attributes, merge=True)
    if publish:
        published_message = deepcopy(attributes)
        if message_formatter is not None:
            published_message = message_formatter(published_message)
        publish_record_update(record_id=attributes['id'], properties=published_message, collection_name=collection_name,
                              action='add')
    if batch is not None:
        return attributes, batch
    else:
        return attributes
