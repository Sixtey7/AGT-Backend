from model.database import db
from model.models import Item
from uuid import uuid4


def get_all():
    """Returns all of the Item objects in the database

    :return A list of Item objects
    :rtype list
    """
    return Item.query.all()


def get(item_id):
    """Returns the Item object specified by the provided id

    :param item_id: The id of the Item to retrieve, nominally a uuid
    :return A single Item object
    :rtype Item
    """
    return Item.query.filter_by(id=item_id).first()


def create(name, item_id=None):
    """Creates a Item given the provided values

    :param name: The string name of the Item object
    :param item_id: The id to assign to the Item.  If not provided, a uuid will be generated
    :return The created Item object
    :rtype Item
    """

    if item_id is None:
        item_id = str(uuid4())

    new_item = Item(id=item_id, name=name)

    db.session.add(new_item)
    db.session.commit()

    return new_item


def update(item_id, name):
    """Updates the specified Item with the provided value

    :param item_id: The id of the Item to be updated
    :param name: The name to assigned to the specified Item
    :return The updated Item object
    :rtype Item
    :raise ValueError if the Item cannot be found
    """

    item_to_update = Item.query.filter_by(id=item_id).first()

    if item_to_update is None:
        raise ValueError("Could not find Item with provided id %s" % item_id)

    item_to_update.name = name

    db.session.commit()

    return item_to_update


def delete(item_id):
    """Deletes the Item specified by the provided item_id
    
    :param item_id: The id of the Item to be deleted
    :return True if the Item was successfully deleted
    :raise ValueError if the Item could not be found
    """

    item_to_delete = Item.query.filter_by(id=item_id).first()

    if item_to_delete is None:
        raise ValueError("Could not find Item with id")

    db.session.delete(item_to_delete)
    db.session.commit()

    return True
