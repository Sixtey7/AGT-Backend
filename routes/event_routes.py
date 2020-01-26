from flask import Blueprint, abort, jsonify, request
import model.EventDB as EventDB

event_api = Blueprint('event_api', __name__)


@event_api.route('', methods=['GET'])
def get_all():
    """Returns all of the Events that exist in the database

    :return the result as a json array
    """
    return jsonify([event.to_obj() for event in EventDB.get_all()]), 200


@event_api.route('<string:event_id>', methods=['GET'])
def get(event_id):
    """Returns the Event specified by the provided event_id

    :param event_id: The id of the Event to return
    :return 200 and the specified Event object, or 404 if no event was found with the event_id
    """
    event_obj = EventDB.get(event_id)
    if event_id is None:
        abort(404, 'No Event was found with the provided id!')

    return jsonify(event_obj.to_obj()), 200


@event_api.route('', methods=['POST'])
def create():
    """Used to create an Event

    Expects the details of the Event in JSON format as part of the request body
    If no id is provided, an id will be generated as part of the Event creation

    :return 200 and the newly created Event or 400 if no request body was found
    """
    if not request.json:
        abort(400, 'No request body was provided!')

    event = EventDB.create(request.json['item_id'],
                           request.json['value'],
                           request.json['date'],
                           request.json['id'] if 'id' in request.json else None)

    return jsonify(event.to_obj()), 200


@event_api.route('<string:event_id>', methods=['PUT'])
def update(event_id):
    """Updates the specified Event with the contents of the request body (in JSON)

    :param event_id: The id of the Event to be updated
    :return 200 and the updated Event, 400 if no request body has been provided
        404 if the specified Event cannot be found
    """
    if not request.json:
        abort(400, 'No request body provided')

    try:
        event = EventDB.update(event_id,
                               request.json['item_id'] if 'item_id' in request.json else None,
                               request.json['value'] if 'value' in request.json else None,
                               request.json['date'] if 'date' in request.json else None)

        return jsonify(event.to_obj()), 200
    except ValueError:
        abort(404, 'Could not find Event with provided id')


@event_api.route('<string:event_id>', methods=['DELETE'])
def delete(event_id):
    """Deletes the specified Event from the database

    :param event_id: The id of the Event to be deleted
    :return 200 if the Event was successfully deleted, 404 if the Event cannot be found"""
    try:
        status = EventDB.delete(event_id)
        if status:
            return '', 200
        else:
            return '', 500
    except ValueError:
        abort(404, 'Could not find Event with the provided id')
