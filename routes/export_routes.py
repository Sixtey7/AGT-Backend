from flask import Blueprint, request, abort
import utils.Exporter as Exporter

export_api = Blueprint('export_api', __name__)


@export_api.route('', methods=['GET'])
def export_all():
    """Exports all of the data in the database as a CSV File

    :return the contents of the database as comma-seperated-values
    """
    export_return = Exporter.export_all_data()

    return export_return, 200


@export_api.route('', methods=['PUT'])
def import_all():
    """Imports all of the data into the database from a CSV file
    """
    print (request.data)
    if not request.data:
        abort(400, 'No request body provided')

    Exporter.import_all_date(request.data)
