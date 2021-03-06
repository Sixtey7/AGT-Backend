from flask import Blueprint, abort, jsonify, request
import model.ItemDB as ItemDB

item_api = Blueprint('item_api', __name__)


@item_api.route('', methods=['GET'])
def get_all():
    """Returns all of the Items that exist in the database

    :return the result as a json array
    """
    return jsonify([item.to_obj() for item in ItemDB.get_all()]), 200


@item_api.route('<string:item_id>', methods=['GET'])
def get(item_id):
    """Returns the Item specified by the provided item_id

    :param item_id: The id of the Item to return
    :return 200 and the specified Item object, or 404 if no item was found with the provided id
    """
    item_obj = ItemDB.get(item_id)
    if item_obj is None:
        abort(404, 'No Item was found for the provided id!')

    print(item_obj)
    return jsonify(item_obj.to_obj()), 200


@item_api.route('', methods=['POST'])
def create():
    """Used to create a new Item.

    Expects the details of the Item in JSON format as part of the request body
    If no id is provided, an id will be generated as part of the Item creation

    :return 200 and the newly created Item or 400 if no request body was found
    """
    if not request.json:
        abort(400, 'No request body was provided!')

    item = ItemDB.create(request.json['name'],
                         request.json['category_id'],
                         request.json['item_type'],
                         request.json['current_value'],
                         request.json['goal_value'],
                         request.json['id'] if 'id' in request.json else None,
                         request.json['goal_date'] if 'goal_date' in request.json else None)

    return jsonify(item.to_obj()), 200


@item_api.route('<string:item_id>', methods=['PUT'])
def update(item_id):
    """Updates the specified Item with the contents of the request body (in JSON)
    
    :param item_id: The id of the Item to be updated
    :return 200 and the updated Item, 400 if no request body has been provided
        404 if the specified Item cannot be found
    """
    if not request.json:
        abort(400, 'No request body provided')

    try:
        item = ItemDB.update(item_id,
                             request.json['name'] if 'name' in request.json else None,
                             request.json['category_id'] if 'category_id' in request.json else None,
                             request.json['item_type'] if 'item_type' in request.json else None,
                             request.json['current_value'] if 'current_value' in request.json else None,
                             request.json['goal_value'] if 'goal_value' in request.json else None,
                             request.json['goal_date' if 'goal_date' in request.json else None])

        return jsonify(item.to_obj()), 200
    except ValueError:
        abort(404, 'Could not find Item with provided id')


@item_api.route('<string:item_id>', methods=['DELETE'])
def delete(item_id):
    """Deletes the specified Item from the database

    :param item_id: The id of the Item to be deleted
    :return 200 if the Item was successfully deleted, 404 if the Item cannot be found
    """
    try:
        status = ItemDB.delete(item_id)
        if status:
            return '', 200
        else:
            return '', 500
    except ValueError:
        abort(404, 'Could not find Item with the provided id')
