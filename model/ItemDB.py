from model.database import db
from model.models import Item
from uuid import uuid4
from datetime import date


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


def create(name, category_id, item_type, current_value, goal_value, item_id=None, goal_date=None):
    """Creates a Item given the provided values

    :param name: The string name of the Item object
    :param category_id: The id of the category that the Item belongs to
    :param item_type: The type of Item this is
    :param current_value: The current value of the Item
    :param goal_value: The goal value for the item
    :param item_id: The id to assign to the Item.  If not provided, a uuid will be generated
    :param goal_date: The goal date to assign to the Item.  If not provided, it will be omitted from the entry
    :return The created Item object
    :rtype Item
    """

    if item_id is None:
        item_id = str(uuid4())

    if goal_date is None:
        new_item = Item(id=item_id, name=name, category_id=category_id, item_type=item_type,
                        current_value=current_value, goal_value=goal_value)
    else:
        date_parts = [int(x) for x in goal_date.split('-')]
        # TODO: should probably eventually add some validation here
        date_obj = date(date_parts[0], date_parts[1], date_parts[2])

        new_item = Item(id=item_id, name=name, category_id=category_id, item_type=item_type,
                        current_value=current_value, goal_value=goal_value, goal_date=date_obj)

    db.session.add(new_item)
    db.session.commit()

    return new_item


def update(item_id, name, category_id, item_type, current_value, goal_value):
    """Updates the specified Item with the provided value

    :param item_id: The id of the Item to be updated
    :param name: If provided, the name to set the specified Item to
    :param category_id: If provided, the category_id to set the specified Item to
    :param item_type: If provided, the item_type to set the specified Item to
    :param current_value: If provided, the current_value to set the specified Item to
    :param goal_value: If provided, the goal_value to set the specified Item to
    :return The updated Item object
    :rtype Item
    :raise ValueError if the Item cannot be found
    """

    item_to_update = Item.query.filter_by(id=item_id).first()

    if item_to_update is None:
        raise ValueError("Could not find Item with provided id %s" % item_id)

    if name is not None:
        item_to_update.name = name

    if category_id is not None:
        item_to_update.category_id = category_id

    if item_type is not None:
        item_to_update.item_type = item_type

    if current_value is not None:
        item_to_update.current_value = current_value

    if goal_value is not None:
        item_to_update.goal_value = goal_value

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
