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
    # Nursing home data
    df = pd.DataFrame(dict(
        date=["2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10"],
        happiness=[75, 78, 81, 71, 74, 79]
    ))
    # National Data
    df2 = pd.DataFrame(dict(
        date=["2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10"],
        happiness=[67, 75, 84, 64, 71, 75]
    ))
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="Happiness Proportion - Macquarie Nursing Home",x=df["date"], y=df["happiness"]))
    fig.add_trace(go.Scatter(name="Happiness Proportion - National Average",x=df2["date"], y=df2["happiness"]))
    fig.update_layout(
                width=580,
                height=280,
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    activity=["Cycling", "Travelling", "Boating", "Write Diary", "Drinking", "Playing the piano"]
    activity_frequency=[15, 17, 9, 12, 11,15]

    activities_bar_chart = go.Figure(data=[go.Bar(x=activity, y=activity_frequency)])
    activities_bar_chart.update_layout(
                width=580,
                height=280,
    )
    graphJSON_activities = json.dumps(activities_bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    num_elderly = 4
    emoji_name = "Happy"
    activity_name = "Drinking"
    percentage_happiness = 80

    return render_template("outputs.html", user=current_user, graphJSON=graphJSON, graphJSON_activities=graphJSON_activities, num_elderly=num_elderly,
        emoji_name = emoji_name, activity_name=activity_name, percentage_happiness=percentage_happiness)


@views.route('/instructions', methods=['GET'])
@login_required
def instruction():
    return render_template("instruction.html", user=current_user)


@views.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@views.route('/edit-input-options', methods=['GET', 'POST'])
@login_required
def edit_input_options():
    return render_template("edit_input.html", user=current_user)


# @views.route('/temporary-inputs', methods=['GET', 'POST'])
# @login_required
# def temporary_input():
#     return render_template("temporary-inputs-presentation.html", user=current_user)


# @views.route('/temporary-outputs', methods=['GET', 'POST'])
# @login_required
# def temporary_output():
#     return render_template("temporary-outputs-presentation.html", user=current_user)


@views.route('/guest-inputs', methods=['GET', 'POST'])
@login_required
def guest_inputs():
    return render_template("guest_inputs.html", user=current_user)

@views.route('/home_user', methods=['GET', 'POST'])
@login_required
def home_user():
    return render_template("home_user.html", user=current_user)