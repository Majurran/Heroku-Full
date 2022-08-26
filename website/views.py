from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
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

@views.route('/inputs', methods=['GET', 'POST'])
@login_required
def user_input_page():
    return render_template("inputs.html", user=current_user)


@views.route('/outputs', methods=['GET'])
@login_required
def dashboard_page():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    })
    fig = px.bar(df, x="Fruit", y="Number Eaten", color="Contestant", barmode="group")
    fig.update_yaxes(title_text="Number Eaten")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("outputs.html", user=current_user, graphJSON=graphJSON)


@views.route('/instructions', methods=['GET'])
@login_required
def instruction():
    return render_template("instruction.html", user=current_user)


@views.route('/edit_input_options', methods=['GET', 'POST'])
@login_required
def edit_input_options():
    return render_template("edit_input.html", user=current_user)