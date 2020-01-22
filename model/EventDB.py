from model.database import db
from model.models import Event
from uuid import uuid4


def get_all():
    """Returns all of the Event objects in the database

    :return A list of Event objects
    :rtype list
    """
    return Event.query.all()


def get(event_id):
    """Returns the Event object specified by the provided id

    :param event_id: The id of the Event to retrieve, nominally a uuid
    :return A single Event object
    :rtype Event
    """
    return Event.query.filter_by(id=event_id).first()


def create(name, event_id=None):
    """Creates a Event given the provided values

    :param name: The string name of the Event object
    :param event_id: The id to assign to the Event.  If not provided, a uuid will be generated
    :return The created Event object
    :rtype Event
    """

    if event_id is None:
        event_id = str(uuid4())

    new_event = Event(id=event_id, name=name)

    db.session.add(new_event)
    db.session.commit()

    return new_event


def update(event_id, name):
    """Updates the specified Event with the provided value

    :param event_id: The id of the Event to be updated
    :param name: The name to assigned to the specified Event
    :return The updated Event object
    :rtype Event
    :raise ValueError if the Event cannot be found
    """

    event_to_update = Event.query.filter_by(id=event_id).first()

    if event_to_update is None:
        raise ValueError("Could not find Event with provided id %s" % event_id)

    event_to_update.name = name

    db.session.commit()

    return event_to_update


def delete(event_id):
    """Deletes the Event specified by the provided event_id
    
    :param event_id: The id of the Event to be deleted
    :return True if the Event was successfully deleted
    :raise ValueError if the Event could not be found
    """

    event_to_delete = Event.query.filter_by(id=event_id).first()

    if event_to_delete is None:
        raise ValueError("Could not find Event with id")

    db.session.delete(event_to_delete)
    db.session.commit()

    return True
