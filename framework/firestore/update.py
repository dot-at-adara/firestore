def format_update_message(attributes):
    update = dict()
    for k, v in attributes.items():
        if isinstance(v, dict):
            for key, value in format_update_message(v).items():
                update['{0}.{1}'.format(k, key)] = value
        else:
            update[k] = v
    return update


def update_object(collection_name: str, object_id, attributes: dict, batch=None, publish=False, message_formatter=None,
                  user_id=None, upsert=False, override=False, overwrite_updated=False):
    from handlers.core.collections import publish_record_update
    from handlers.core.firestore.base import create_db_client
    from server import collections, collection_schemas
    from datetime import datetime
    from copy import deepcopy
    db = create_db_client()
    doc_ref = db.collection(collections[collection_name]).document(object_id)
    now = datetime.utcnow()
    attributes = deepcopy(attributes)
    if not overwrite_updated:
        attributes['updated'] = now

    if not override:
        attributes = format_update_message(attributes=attributes)

    if batch is not None:
        if upsert:
            batch.set(doc_ref, attributes, merge=True)
        else:
            batch.update(doc_ref, attributes)
    else:
        if upsert:
            doc_ref.set(attributes, merge=True)
        else:
            doc_ref.update(attributes)
    if not batch:
        attributes = doc_ref.get().to_dict()
    if publish and batch is None:
        published_message = deepcopy(attributes)
        if message_formatter is not None:
            published_message = message_formatter(published_message)
        publish_record_update(record_id=published_message['id'], properties=published_message,
                              collection_name=collection_name,
                              action='update')
    elif publish and batch is not None:
        raise ValueError("Cannot publish updates in batch mode as they have not been committed yet")
    if batch is not None:
        return attributes, batch
    else:
        return attributes


def delete_object(collection_name, object_id, publish=False, batch=None, user_id=None):
    from handlers.core.collections import publish_record_update
    attributes = dict(id=object_id, active=False)
    results = update_object(collection_name=collection_name, object_id=object_id, attributes=attributes, batch=batch,
                            publish=False)
    if publish:
        publish_record_update(record_id=attributes['id'], properties=attributes, collection_name=collection_name,
                              action='delete')
    return results
