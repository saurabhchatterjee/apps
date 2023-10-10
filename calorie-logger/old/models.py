import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Food(db.Model):
    # TODO: database for any food item I use
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    food_item = sa.Column(sa.String, nullable=False)
    pass


class Activity(db.Model):
    # TODO: add activities here
    pass


class FoodLogger(db.Model):
    # TODO: track food intake daily
    pass


class ActivityLogger(db.Model):
    # TODO: track type of activity, duration, calories burned and any special notes
    pass


class WellnessLogger(db.Model):
    # TODO: track sleep, mood, other non tangibles
    pass
