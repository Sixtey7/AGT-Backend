from flask import Blueprint
import utils.Exporter as Exporter

export_api = Blueprint('export_api', __name__)


@export_api.route('', methods=['GET'])
def export_all():
    """Exports all of the data in the database as a CSV File

    :return the contents of the database as comma-seperated-values
    """
    export_return = Exporter.export_all_data()

    return export_return, 200
