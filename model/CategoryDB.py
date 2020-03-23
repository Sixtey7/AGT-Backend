from model.database import db
from model.models import Category
from uuid import uuid4


def get_all():
    """Returns all of the Category objects in the database

    :return A list of Category objects
    :rtype list
    """
    return Category.query.all()


def get(category_id):
    """Returns the Category object specified by the provided id

    :param category_id: The id of the Category to retrieve, nominally a uuid
    :return A single Category object
    :rtype Category
    """
    return Category.query.filter_by(id=category_id).first()


def create(name, category_id=None):
    """Creates a Category given the provided values

    :param name: The string name of the Category object
    :param category_id: The id to assign to the Category.  If not provided, a uuid will be generated
    :return The created Category object
    :rtype Category
    """

    if category_id is None:
        category_id = str(uuid4())

    new_category = Category(id=category_id, name=name)

    db.session.add(new_category)
    db.session.commit()

    return new_category


def update(category_id, name):
    """Updates the specified Category with the provided value

    :param category_id: The id of the Category to be updated
    :param name: The name to assigned to the specified Category
    :return The updated Category object
    :rtype Category
    :raise ValueError if the Category cannot be found
    """

    category_to_update = Category.query.filter_by(id=category_id).first()

    if category_to_update is None:
        raise ValueError("Could not find Category with provided id %s" % category_id)

    category_to_update.name = name

    db.session.commit()

    return category_to_update


def delete(category_id):
    """Deletes the Category specified by the provided category_id
    
    :param category_id: The id of the Category to be deleted
    :return True if the Category was successfully deleted
    :raise ValueError if the Category could not be found
    """

    category_to_delete = Category.query.filter_by(id=category_id).first()

    if category_to_delete is None:
        raise ValueError("Could not find Category with id")

    db.session.delete(category_to_delete)
    db.session.commit()

    return True


def delete_all():
    """Deletes all of the Categories in the database
    """

    Category.query.delete()
