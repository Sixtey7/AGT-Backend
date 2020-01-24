from flask import Blueprint, abort, jsonify, request
import model.EventDB as EventDB

event_api = Blueprint('event_api', __name__)


@event_api.route('', methods=['GET'])
def get_all():
    """Returns all of the Events that exist in the database

    :return the result as a json array
    """
    return jsonify([event.to_obj() for event in EventDB.get_all()]), 200
