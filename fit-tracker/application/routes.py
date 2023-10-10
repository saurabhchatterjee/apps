import json
import datetime
from flask import current_app as app
from flask import redirect, render_template, url_for, flash, request, jsonify

import config
from .forms import (AddFoodForm,
                    LogDayForm,
                    SetDayTargetsForm
                    )
from .models import (db,
                     Food,
                     DayLogger,
                     DayTargets
                     )
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)


def __commit_record(record):
    db.session.add(record)
    db.session.flush()
    db.session.commit()


def __jsonify(item, mode="decode"):
    if mode == "encode":
        return json.dumps(item)
    elif mode == "decode":
        return json.loads(item)


@app.route("/")
def index():
    return render_template("index.html",
                           title="Calorie Logger",
                           description="App to track daily calories"
                           )


@app.route("/food/add", methods=["GET", "POST"])
def add_food():
    form = AddFoodForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        qty = form.qty.data
        unit = form.unit.data
        calories = form.calories.data
        fat = form.fat.data
        protein = form.protein.data
        carbs = form.carbs.data
        sugar = form.sugar.data
        added_sugar = form.added_sugar.data
        record = Food(name=name, description=description, qty=qty, unit=unit,
                      calories=calories, fat=fat, protein=protein, carbs=carbs, sugar=sugar,
                      added_sugar=added_sugar)
        __commit_record(record)
        flash(
            f'{form.name.data} added successfully.',
            'success'
        )
        return redirect(url_for('index'))
    return render_template("add_food.html", form=form)


@app.route("/food/view")
def view_all_food():
    records = db.session.query(Food).all()
    columns = ['Id', 'Name', 'Description', 'Quantity',
               'Unit', 'Calories', 'Fat', 'Protein',
               'Carbs', 'Sugar', 'Added Sugar']
    return render_template("view_food.html", foods=records, columns=columns)


@app.route("/log/set_day_targets", methods=["GET", "POST"])
def set_day_target():
    form = SetDayTargetsForm()
    hashed_id = app.config.get('DB_HASH')
    record = db.session.query(DayTargets).filter_by(dt_id=hashed_id).first()
    target_set = record is not None
    if target_set:
        flash(f"Targets already set for {app.config.get('TODAY')}.", 'error')
        return redirect(url_for('index'))
    if request.method == "POST" and form.validate_on_submit():
        calorie = form.calorie_target.data
        fat = form.fat_target.data
        protein = form.protein_target.data
        carbs = form.carbs_target.data
        if "copy_week" in request.form:
            today = datetime.date.today()
            all_hashes = [config.create_hash(today)]
            for i in range(1, 7):
                data = today + datetime.timedelta(i)
                all_hashes.append(config.create_hash(data))
            for hash_id in all_hashes:
                target = DayTargets(
                    dt_id=hash_id,
                    cal_tgt=calorie,
                    f_tgt=fat,
                    p_tgt=protein,
                    c_tgt=carbs
                )
                __commit_record(target)
            flash(f"Targets successfully set for the week.", 'success')
        else:
            target = DayTargets(
                dt_id=hashed_id,
                cal_tgt=form.calorie_target.data,
                f_tgt=form.fat_target.data,
                p_tgt=form.protein_target.data,
                c_tgt=form.carbs_target.data
            )
            __commit_record(target)
            flash(f"Targets successfully set for {app.config.get('TODAY')}.", 'success')
        return redirect(url_for('index'))

    return render_template('set_day_targets.html',
                           form=form,
                           today=app.config.get('TODAY')
                           )


@app.route("/log/day", methods=["GET", "POST"])
def day_log():
    hashed_id = app.config.get('DB_HASH')

    day_target_record = db.session.query(DayTargets).filter_by(dt_id=hashed_id).first()
    has_target_set = day_target_record is not None
    if not has_target_set:
        flash(f"{app.config.get('TODAY')} has no targets set. Redirecting to set targets.", 'error')
        return redirect(url_for('set_day_target'))
    else:
        day_log_record = db.session.query(DayLogger).filter_by(d_id=hashed_id).first()
        has_food_data = day_log_record is not None
        # print(f"has_food_data: {has_food_data}")
        form = LogDayForm()

        if request.method == 'POST':
            if 'done' in request.form:
                flash(f"Food logged successfully for {app.config.get('TODAY')}.", 'success')
                return redirect(url_for('index'))
            elif 'log_food' in request.form and form.validate_on_submit():
                logger_record_list = []
                for food in form.foods.entries:
                    food_id, food_dict = __extract_food_data(food)
                    if has_food_data:
                        # print("has food data nd logging in existing")
                        existing_data = __jsonify(day_log_record.d_list, mode='decode')
                        # print(f"existing_data: {existing_data}")
                        existing_data.append(food_dict)
                        # print(f"existing_data now: {existing_data}")
                        day_log_record.d_list = __jsonify(existing_data, mode='encode')
                        db.session.flush()
                        db.session.commit()
                        # print(f"day_log_record.d_list: {day_log_record.d_list}")
                    else:
                        logger_record_list.append(food_dict)
                        logger_data = DayLogger(d_id=hashed_id, d_list=__jsonify(logger_record_list, mode='encode'))
                        __commit_record(logger_data)
                        # day_log_record1 = db.session.query(DayLogger).filter_by(d_id=hashed_id).first()
                        # print(f"after commit: {day_log_record1.d_list}")

                flash(f"{app.config.get('TODAY')} logged successfully.", 'success')

        updated_records = db.session.query(DayLogger).filter_by(d_id=hashed_id).first()
        food_records = None if not updated_records else __jsonify(updated_records.d_list, mode='decode')
        remaining_macros = __get_remaining_macros(hashed_id, food_records)

        return render_template("day_log1.html",
                               form=form,
                               today=app.config.get('TODAY'),
                               columns=['Day', 'Food Name', 'Unit', 'Quantity', 'Description', 'Calories', 'Fat',
                                        'Protein',
                                        'Carbs', 'Sugar', 'Added Sugar'],
                               has_food_data=has_food_data,
                               food_records=food_records,
                               has_target_set=has_target_set,
                               target=day_target_record,
                               remaining_macros=remaining_macros
                               )


@app.route("/log/query", methods=['POST'])
def query_food():
    print(request.form.items())
    food_id = request.form.get('selected_food')
    food_qty = int(request.form.get('input_qty'))
    record = db.session.query(Food).filter_by(f_id=food_id).first()
    output = {'unit': record.f_unit,
              'description': record.f_description,
              'calories': int((record.f_calories / record.f_qty) * food_qty),
              'fat': int((record.f_fat / record.f_qty) * food_qty),
              'protein': int((record.f_protein / record.f_qty) * food_qty),
              'carbs': int((record.f_carbs / record.f_qty) * food_qty),
              'sugar': int((record.f_sugar / record.f_qty) * food_qty),
              'added_sugar': int((record.f_added_sugar / record.f_qty) * food_qty)
              }
    print(output)
    return jsonify(output)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    hashed_id = app.config.get('DB_HASH')
    updated_records = db.session.query(DayLogger).filter_by(d_id=hashed_id).first()
    food_records = None if not updated_records else __jsonify(updated_records.d_list, mode='decode')
    totals = {'calories': 0, 'fat': 0, 'protein': 0, 'carbs': 0, 'sugar': 0, 'added_sugar': 0}
    if food_records is not None:
        for food in food_records:
            totals['calories'] += food['calories']
            totals['fat'] += food['fat']
            totals['protein'] += food['protein']
            totals['carbs'] += food['carbs']
            totals['sugar'] += food['sugar']
            totals['added_sugar'] += food['added_sugar']

    return render_template("dashboard.html",
                           columns=['Day', 'Food Name', 'Unit', 'Quantity',
                                    'Description', 'Calories', 'Fat',
                                    'Protein', 'Carbs', 'Sugar', 'Added Sugar'],
                           has_food_data=food_records is not None,
                           food_records=food_records,
                           today=app.config.get('TODAY'),
                           totals=False if food_records is None else totals
                           )


def __get_remaining_macros(hashed_id, records):
    targets = db.session.query(DayTargets).filter_by(dt_id=hashed_id).first()
    remaining_macros = {'calorie': targets.calorie_target,
                        'fat': targets.fat_target,
                        'protein': targets.protein_target,
                        'carbs': targets.carbs_target}
    if records is not None:
        for record in records:
            remaining_macros['calorie'] -= record['calories']
            remaining_macros['fat'] -= record['fat']
            remaining_macros['protein'] -= record['protein']
            remaining_macros['carbs'] -= record['carbs']

    return remaining_macros


def __extract_food_data(field):
    food_id = field.item.data
    food_name = (db.session.query(Food).filter_by(f_id=food_id).first()).f_name
    food_qty = field.quantity.data
    record = db.session.query(Food).filter_by(f_id=food_id).first()
    unit = record.f_unit
    description = record.f_description
    calories = int((record.f_calories / record.f_qty) * food_qty)
    fat = int((record.f_fat / record.f_qty) * food_qty)
    protein = int((record.f_protein / record.f_qty) * food_qty)
    carbs = int((record.f_carbs / record.f_qty) * food_qty)
    sugar = int((record.f_sugar / record.f_qty) * food_qty)
    added_sugar = int((record.f_added_sugar / record.f_qty) * food_qty)
    d = {'id': food_id,
         'name': food_name,
         'qty': food_qty,
         'unit': unit,
         'description': description,
         'calories': calories,
         'fat': fat,
         'protein': protein,
         'carbs': carbs,
         'sugar': sugar,
         'added_sugar': added_sugar
         }
    return food_id, d
