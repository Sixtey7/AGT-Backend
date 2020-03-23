import model.CategoryDB as CategoryDB
import model.ItemDB as ItemDB
import model.EventDB as EventDB
from model.models import ItemType
from uuid import uuid4
from datetime import date


def export_all_data():
    """Facilitates the exporting of all data into CSV format

    :return All of the data in the database in CSV format
    :rtype String
    """

    all_categories = CategoryDB.get_all()

    print("About to print out everything")

    return_string = ""

    for category in all_categories:
        for item in category.items:
            line = ','.join([category.name, item.name, item.current_value, item.goal_value,
                             item.item_type.value_string(), str(item.goal_date)])
            line += ','
            if len(item.events) > 0:
                line += ';'.join([str(event.date) for event in item.events])

            return_string += line + '\n'

    print(return_string)
    print("Finished printing out everything")

    return return_string


def import_all_date(input_string):
    """Facilitates the importing of all data from a CSV format

    Clears out the database prior to running

    :param input_string: A string containing the data to be imported
    """
    # totally clear out the database prior to starting the import
    print('Clearing out the database')
    _delete_all_elements()

    # parse the input
    print('Got the input string %s' % input_string)
    all_lines = [s.strip() for s in input_string.splitlines()]
    print('Got %d lines' % len(all_lines))

    category_dict = {}
    for line in all_lines:
        all_rows = line.split(',')
        print('found %d rows' % len(all_rows))
        category_name = all_rows[0]
        item_name = all_rows[1]
        current_value = all_rows[2]
        goal_value = all_rows[3]
        item_type = all_rows[4]
        goal_date = all_rows[5]

        # build a random id for the item
        item_id = str(uuid4())

        # parse the value for the item type into the object
        item_type_obj = ItemType(value=int(item_type))

        # determine if this is a category we've met before
        if category_name in category_dict:
            category_id = category_dict[category_name]
        else:
            # this is a new category, assign it an id
            category_id = str(uuid4())
            category_dict[category_name] = category_id
            # Persist the built category
            CategoryDB.create(category_id=category_id, name=category_name)

        # Persist the built item object
        ItemDB.create(item_id=item_id, name=item_name, category_id=category_id,
                      item_type=item_type_obj, current_value=current_value,
                      goal_value=goal_value, goal_date=goal_date)
        # check if there are events to be parsed into event objects
        if len(all_rows) == 7:
            events_string = all_rows[6]
            if events_string != '':
                # ; is used to separate the dates in the event string
                event_date_array = events_string.split(';')
                # loop through all of the dates and build event objects
                for event_date in event_date_array:
                    # Persist the built event object
                    EventDB.create(event_id=str(uuid4()), item_id=item_id, value="True",
                                   event_date=event_date)


def _build_date_obj(date_str):
    """Helper method used to decompose the date strings in the export into date objects

    :param date_str: The date string in format YYYY-MM-DD
    :return: Date object based on the provided value
    :rtype: date
    """
    print('parsing date_str %s' % date_str)
    date_parts = [int(x) for x in date_str.split('-')]
    date_obj = date(date_parts[0], date_parts[1], date_parts[2])

    return date_obj


def _delete_all_elements():
    """Cleans out the database of all existing entries
    """
    EventDB.delete_all()
    ItemDB.delete_all()
    CategoryDB.delete_all()
