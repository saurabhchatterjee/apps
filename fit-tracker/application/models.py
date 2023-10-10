from . import db
import sqlalchemy as sa


class Food(db.Model):
    __tablename__ = "food"
    f_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    f_name = sa.Column(sa.String, nullable=False)
    f_description = sa.Column(sa.String, nullable=False)
    f_qty = sa.Column(sa.Integer, nullable=False, default=0)
    f_unit = sa.Column(sa.String, nullable=False, default=0)
    # macros
    f_calories = sa.Column(sa.Integer, nullable=False, default=0)
    f_fat = sa.Column(sa.Integer, nullable=False, default=0)
    f_protein = sa.Column(sa.Integer, nullable=False, default=0)
    f_carbs = sa.Column(sa.Integer, nullable=False, default=0)
    f_sugar = sa.Column(sa.Integer, nullable=False, default=0)
    f_added_sugar = sa.Column(sa.Integer, nullable=False, default=0)

    def __init__(self, name, description, qty, unit, calories, fat, protein, carbs, sugar, added_sugar):
        self.f_name = name
        self.f_description = description
        self.f_qty = qty
        self.f_unit = unit
        self.f_calories = calories
        self.f_fat = fat
        self.f_protein = protein
        self.f_carbs = carbs
        self.f_sugar = sugar
        self.f_added_sugar = added_sugar


class DayLogger(db.Model):
    d_id = sa.Column(sa.String, primary_key=True)
    d_list = sa.Column(sa.String, nullable=True)

    def __init__(self, d_id, d_list):
        self.d_id = d_id
        self.d_list = d_list


class DayTargets(db.Model):
    dt_id = sa.Column(sa.String, primary_key=True)
    calorie_target = sa.Column(sa.Integer, nullable=False, default=0)
    fat_target = sa.Column(sa.Integer, nullable=False, default=0)
    protein_target = sa.Column(sa.Integer, nullable=False, default=0)
    carbs_target = sa.Column(sa.Integer, nullable=False, default=0)

    def __init__(self, dt_id, cal_tgt, f_tgt, p_tgt, c_tgt):
        self.dt_id = dt_id
        self.calorie_target = cal_tgt
        self.fat_target = f_tgt
        self.protein_target = p_tgt
        self.carbs_target = c_tgt
