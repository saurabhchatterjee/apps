from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddFoodItemForm(FlaskForm):
    item = StringField("food_item", validators=[DataRequired()])
    # TODO: add more fields required to add a new item


class AddNewActivityForm(FlaskForm):
    # TODO: add new activity fields
    pass


class LogFoodForm(FlaskForm):
    # TODO: create form to log food
    pass


class LogActivityForm(FlaskForm):
    # TODO: create form to log activity
    pass


class LogWellnessForm(FlaskForm):
    # TODO: create form to log wellness
    pass
