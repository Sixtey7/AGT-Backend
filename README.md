# AGT-Backend

## Annual Goal Tracker - Backend
Backend of an annual goal tracking application written in Python using Flask and SQLAlchemy.  

Allows a user to create and track goals of things they want to accomplish over the course of the year.  

This includes two types of goals:
* An item in which the item is completed in one fell swoop (Pay off a loan)
* Items that need to be tracked over the course of the year (e.g. go to the gym 50 times)
    * These can be both positive and negative (e.g. drink less than 50 cans of soda)


## Related Projects
[AGT-Frontend](https://github.com/Sixtey7/AGT-Frontend)

## Tools Used
Installed the following through pip3
* flask
* sqlalchemy
* flask-sqlalchemy

## Example Curl Statements

### Categories

#### Add a new
* curl -H "Content-type: application/json" -i -XPOST -d '{"name":"Sample"}' http://localhost:5000/categories/

### Items
#### Add a new
* curl -H "Content-type: application/json" -i -XPOST -d '{"name": "Item 1", "category_id": "800e11e8-da24-4caf-a854-fa0a4efd751e", "item_type": "one_and_done", "current_value":"false", "goal_value": "true", "goal_date":"2020-01-30"}' http://localhost:5000/items/
