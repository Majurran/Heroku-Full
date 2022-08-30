from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
# from .models import Note
from . import db
import json
import plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

# Don't need for project, but can keep for comments as reference for now
# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})

@views.route('/inputs', methods=['GET'])
@login_required
def user_input_page():
    return render_template("inputs.html", user=current_user)

@views.route('/inputs', methods=['POST'])
@login_required
def user_input_page_post():
    my_var = request.form.get('json')
    print(my_var)
    return render_template("inputs.html", user=current_user)

@views.route('/outputs', methods=['GET'])
@login_required
def dashboard_page():
    df = pd.DataFrame(dict(
        date=["2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10"],
        happiness=[75, 78, 81, 71, 74, 79]
    ))
    df2 = pd.DataFrame(dict(
        date=["2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10"],
        happiness=[67, 75, 84, 64, 71, 75]
    ))
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="Happiness Proportion - Macquarie Nursing Home",x=df["date"], y=df["happiness"]))
    fig.add_trace(go.Scatter(name="Happiness Proportion - National Average",x=df2["date"], y=df2["happiness"]))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("outputs.html", user=current_user, graphJSON=graphJSON)


@views.route('/instructions', methods=['GET'])
@login_required
def instruction():
    return render_template("instruction.html", user=current_user)


@views.route('/edit-input-options', methods=['GET', 'POST'])
@login_required
def edit_input_options():
    return render_template("edit_input.html", user=current_user)

@views.route('/temporary-inputs', methods=['GET', 'POST'])
@login_required
def temporary_input():
    return render_template("temporary-inputs-presentation.html", user=current_user)

@views.route('/temporary-outputs', methods=['GET', 'POST'])
@login_required
def temporary_output():
    return render_template("temporary-outputs-presentation.html", user=current_user)