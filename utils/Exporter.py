import model.CategoryDB as CategoryDB
from model.models import Event, Item
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
            line = ','.join([category.name, item.name, item.current_value, str(item.goal_date)])
            line += ','
            if len(item.events) > 0:
                line += ';'.join([str(event.date) for event in item.events])

            return_string += line + '\n'

    print(return_string)
    print("Finished printing out everything")

    return return_string


def import_all_date(input_string):
    """Facilitates the importing of all data from a CSV format

    :param input_string: A string containing the data to be imported
    """
    print('Got the input string %s' % input_string)
    all_lines = [s.strip() for s in input_string.splitlines()]
    print('Got %d lines' % len(all_lines))

    for line in all_lines:
        all_rows = line.split(',')
        print('found %d rows' % len(all_rows))
        category_name = all_rows[0]
        item_name = all_rows[1]
        current_value = all_rows[2]
        goal_date = all_rows[3]

        # Split the event string into an array of event dates
        item_id = uuid4()
        # TODO: Need to figure out category ids
        # TODO: Need to figure out item type
        # TODO: Need to add in goal_value
        print('Date: ' + goal_date)
        goal_date_obj = _build_date_obj(goal_date)
        new_item = Item(id=item_id, name=item_name, category_id=uuid4(),
                        item_type='tracked_positive', current_value=current_value,
                        goal_value='5', goal_date=goal_date_obj)
        print('built the item: ' + new_item.__str__())
        event_array = []
        if len(all_rows) == 5:
            events_string = all_rows[4]
            if events_string != '':
                event_date_array = events_string.split(';')
                for event_date in event_date_array:
                    event_date_obj = _build_date_obj(event_date)
                    new_event = Event(id=uuid4(), item_id=item_id,
                                      value="True", date=event_date_obj)
                    print('built the event: ' + new_event.__str__())


def _build_date_obj(date_str):
    print('parsing date_str %s' % date_str)
    date_parts = [int(x) for x in date_str.split('-')]
    date_obj = date(date_parts[0], date_parts[1], date_parts[2])

    return date_obj
