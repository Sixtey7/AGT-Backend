import model.CategoryDB as CategoryDB


def export_all_data():
    """Facilitates the exporting of all data into CSV format

    :return All of the data in the database in CSV format
    :rtype String
    """

    all_categories = CategoryDB.get_all()

    print("About to print out everything")
    # TODO: Flesh out this proof of concept
    for category in all_categories:
        for item in category.items:
            for event in item.events:
                print(event.date)

    print("Finished printing out everything")
