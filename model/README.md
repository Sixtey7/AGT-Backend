# Models

## Description
Holds the database related files

## Design
### Category
* id
    * UUID
* name
    * string
* items
    * list of Item

### Item
* id
    * UUID
* name
    * string
* category id
    * UUID
* type
    * Enum
        * One and Done
        * Tracked Positive
        * Tracked Negative
* current_value 
    * string
* goal_value
    * string
* goal_date
    * date
* events
    * list of Event
    
### Event
* id
    * UUID
* category_id
    * UUID
* value
    * string
* date
    * date