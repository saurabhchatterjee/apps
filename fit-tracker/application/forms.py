from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    IntegerField,
    DateTimeField,
    TextAreaField,
    SelectField,
    SubmitField,
    FieldList,
    FormField, HiddenField
)
from wtforms.validators import DataRequired, NumberRange
from .models import Food


class AddFoodForm(FlaskForm):
    name = StringField(label=u'Item Name',
                       validators=[DataRequired()]
                       )
    description = TextAreaField(label=u'Description',
                                validators=[DataRequired()]
                                )
    qty = IntegerField(label=u'Default Quantity',
                       validators=[
                           DataRequired(),
                           NumberRange(min=0)
                       ]
                       )
    unit = SelectField(label=u'Unit',
                       choices=[u'GM', u'ML', u'SLICE']
                       )
    # macros
    calories = IntegerField(label=u'Calories',
                            validators=[
                                DataRequired(),
                                NumberRange(min=0)
                            ]
                            )
    fat = IntegerField(label=u'Fat',
                       validators=[
                           DataRequired(),
                           NumberRange(min=0)
                       ]
                       )
    protein = IntegerField(label=u'Protein',
                           validators=[
                               DataRequired(),
                               NumberRange(min=0)
                           ]
                           )
    carbs = IntegerField(label=u'Carbs',
                         validators=[
                             DataRequired(),
                             NumberRange(min=0)
                         ]
                         )
    sugar = IntegerField(label=u'Sugar',
                         validators=[
                             DataRequired(),
                             NumberRange(min=0)
                         ]
                         )
    added_sugar = IntegerField(label=u'Added Sugar',
                               validators=[
                                   DataRequired(),
                                   NumberRange(min=0)
                               ]
                               )


class FoodRowSubForm(FlaskForm):
    item = SelectField(label=u'Food', coerce=int, choices=[(f.f_id, f.f_name) for f in Food.query.all()])
    quantity = IntegerField(label=u'Quantity', validators=[DataRequired(), NumberRange(min=1)])


class WellnessRowForm(FlaskForm):
    category_name = SelectField(label=u'Category', validators=[DataRequired()], choices=['a', 'b'])
    category_score = SelectField(label=u'Score', validators=[DataRequired()], choices=[1, 2, 3, 4, 5])


class ActivityRowForm(FlaskForm):
    activity_name = SelectField(label=u'Activity Name', validators=[DataRequired()], choices=['run', 'workout'])
    activity_duration = IntegerField(label=u'Duration (mins.)', validators=[DataRequired(), NumberRange(min=1)])


class LogDayForm(FlaskForm):
    # TODO: simplify this
    foods = FieldList(FormField(FoodRowSubForm), min_entries=1)
    wellness = FieldList(FormField(WellnessRowForm), min_entries=1)
    activities = FieldList(FormField(ActivityRowForm), min_entries=1)
    csrf_token = HiddenField()


class SetDayTargetsForm(FlaskForm):
    calorie_target = IntegerField(label=u'Calories Target',
                                  validators=[
                                      DataRequired(),
                                      NumberRange(min=0)
                                  ]
                                  )
    fat_target = IntegerField(label=u'Fat Target',
                              validators=[
                                  DataRequired(),
                                  NumberRange(min=0)
                              ]
                              )
    protein_target = IntegerField(label=u'Protein Target',
                                  validators=[
                                      DataRequired(),
                                      NumberRange(min=0)
                                  ]
                                  )
    carbs_target = IntegerField(label=u'Carbs Target',
                                validators=[
                                    DataRequired(),
                                    NumberRange(min=0)
                                ]
                                )
