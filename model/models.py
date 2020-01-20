import enum
from model.database import db
from sqlalchemy import Column, Date, String, ForeignKey, Enum


class Category(db.Model):
    """Model class used to store Category objects in the database
    """
    __tablename__ = "category"
    id = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Category(id='%s', name='%s')>" % (self.id, self.name)

    def to_obj(self):
        """Returns the object in JSON format

        :return: String representation of the object
        """

        return {
            'id': self.id,
            'name': self.name
        }


class ItemType(enum.Enum):
    """Enumeration that stores the types of possible items
    """
    one_and_done = 1
    tracked_positive = 2
    tracked_negative = 2

    def to_json(self):
        """Returns just the name of the value for easy JSON serialization
        """
        return self.name


class Item(db.Model):
    """Model class used to store Item objects in the database
    """
    __tablename__ = 'item'
    id = Column(String, primary_key=True)
    name = Column(String)
    category_id = Column(String, ForeignKey('category.id'))
    item_type = Column(Enum(ItemType))
    current_value = Column(String)
    goal_value = Column(String)
    goal_date = Column(Date)

    def __repr__(self):
        return "<Item(id='%s', name='%s', item_type='%s', category_id='%s', current_value='%s', goal_value='%s'>" % \
               (self.id, self.name, self.item_type, self.category_id, self.current_value, self.goal_value)

    def to_obj(self):
        """Returns the object in JSON format

        :return: String representation of the object
        """

        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'current_value': self.current_value,
            'goal_value': self.goal_value,
            'item_type': self.item_type.to_json(),
            'goal_date': self.goal_date if self.goal_date is not None else ''
        }


class Event:
    """Model class used to store Event objects in the database
    """
    __tablename__ = 'event'
    id = Column(String, primary_key=True)
    category_id = Column(String, ForeignKey('category.id'))
    value = Column(String)
    date = Column(Date)

    def __repr__(self):
        return "<Event(id='%s', category_id='%s', value='%s', date='%s'>" % \
               (self.id, self.category_id, self.value, self.date)

    def to_obj(self):
        """Returns the object in JSON format

        :return: String reprentation of the object
        """

        return {
            'id': self.id,
            'category_id': self.category_id,
            'value': self.value,
            'date': self.date
        }
