from flask import Blueprint, abort, jsonify, request
import model.CategoryDB as CategoryDB

category_api = Blueprint('category_api', __name__)


@category_api.route('', methods=['GET'])
def get_all():
    """Returns all of the Categories that exist in the database

    :return the result as a json array
    """
    return jsonify([category.to_obj() for category in CategoryDB.get_all()]), 200


@category_api.route('<string:category_id>', methods=['GET'])
def get(category_id):
    """Returns the Category specified by the provided category_id

    :param category_id: The id of the Category to return
    :return 200 and the specified Category object, or 404 if no category was found with the provided id
    """
    category_obj = CategoryDB.get(category_id)
    if category_id is None:
        abort(404, 'No Category was found with the provided id!')

    return jsonify(category_obj.to_obj()), 200


@category_api.route('', methods=['POST'])
def create():
    """Used to create a Category

    Expects the details of the Category in JSON format as part of the request body
    If no id is provided, an id will be generated as part of the Category creation

    :return 200 and the newly created Category or 400 if no request body was found
    """
    if not request.json:
        abort(400, 'No request body was provided!')

    category = CategoryDB.create(request.json['name'],
                                 request.json['id'] if 'id' in request.json else None)

    return jsonify(category.to_obj()), 200


@category_api.route('<string:category_id>', methods=['PUT'])
def update(category_id):
    """Updates the specified Category with the contents of the request body (in JSON)

    :param category_id: The id of the Category to be updated
    :return 200 and the updated Category, 400 if no rquest body has been provided
        404 if the specified Category cannot be found
    """
    if not request.json:
        abort(400, 'No request body provided')

    try:
        category = CategoryDB.update(category_id,
                                     request.json['name'])

        return jsonify(category.to_obj()), 200
    except ValueError:
        abort(404, 'Could not find Category with provided id')


@category_api.route('<string:category_id>', methods=['DELETE'])
def delete(category_id):
    """Deletes the specified Category from the database

    :param category_id: The ido f the Category to be deleted
    :return 200 if the Category was successfully deleted, 400 if the Category cannot be found
    """
    try:
        status = CategoryDB.delete(category_id)
        if status:
            return '', 200
        else:
            return '', 500
    except ValueError:
        abort(404, 'Could not find Category with the provided id')
