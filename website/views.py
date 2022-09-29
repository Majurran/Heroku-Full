from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import InputOptions, Input, NursingHome
from . import db
from werkzeug.utils import secure_filename
import json, os, uuid
import plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
views = Blueprint('views', __name__)

# Hyper ref for base.html
ADMIN_HOME_HREF = "/admin"
USER_HOME_HREF = "/user"
GUEST_HOME_HREF = "/guest-inputs"

# Returns Nursing Home name or Guest or User Name for base.html -> "Welcome back, <name>"
def get_name(user):
    if user == "admin" or user == "guest":
        row = NursingHome.query.filter_by(id=current_user.nursing_home_id).first()
        return row.name
    elif user == "resident":
        return current_user.first_name
    else:
        return ""

# ===============================================================================================================
# ==================================================== ADMIN ====================================================
# ===============================================================================================================
@views.route('/', methods=['GET'])
def root():
    return redirect(url_for('auth.login'))


@views.route('/admin', methods=['GET'])
@login_required
def admin_home():
    return render_template("admin/home.html", user=current_user, name=get_name("admin"), home_href=ADMIN_HOME_HREF)


@views.route('/admin/outputs', methods=['GET'])
@login_required
def admin_dashboard_page():
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

    return render_template("admin/outputs.html", user=current_user, graphJSON=graphJSON, graphJSON_activities=graphJSON_activities,
        num_elderly=num_elderly, emoji_name = emoji_name, activity_name=activity_name, percentage_happiness=percentage_happiness, 
        name=get_name("admin"), home_href=ADMIN_HOME_HREF)


@views.route('/admin/instructions', methods=['GET'])
@login_required
def admin_instruction():
    return render_template("admin/instruction.html", user=current_user, name=get_name("admin"), home_href=ADMIN_HOME_HREF)


@views.route('/admin/profile', methods=['GET'])
@login_required
def admin_profile():
    # return render_template("profile.html", user=current_user)
    return render_template("admin/profile_update.html", user=current_user, name=get_name("admin"), home_href=ADMIN_HOME_HREF)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/admin/edit-input-options', methods=['GET', 'POST'])
@login_required
def admin_edit_input_options():
    input_options_rows = InputOptions.query.filter_by(nursing_home_id=current_user.nursing_home_id).all()
    
    if request.method == 'POST':
        # Empty strings returned if no options are selected
        icon_name = request.form.get('iconName')
        category_type = request.form.get('category_type')
        
        # check if the post request has the file part
        if 'image-icon' not in request.files:
            flash('No Image File Selected')
            return redirect(request.url)
        
        image = request.files['image-icon']
        
        # If the user does not select a file, the browser submits an empty file without a filename.
        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # If everything is successful add new input option to database
        if image and allowed_file(image.filename):
            random_characters = str(uuid.uuid1()) + "-" + str(uuid.uuid4())
            filename = secure_filename(random_characters)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
            # Add new Input Option to database
            db_file_path = "/static/input_option_img/" + filename
            new_input_option = InputOptions(category=category_type, name=icon_name, file_path=db_file_path, nursing_home_id=current_user.nursing_home_id)
            db.session.add(new_input_option)
            db.session.commit()
            return redirect(request.url)
        else:
            flash("File extension not allowed, please use the following image format: png, jpg, jpeg, gif")
        
    return render_template("admin/edit_input_ver2.html", user=current_user, name=get_name("admin"), rows=input_options_rows, home_href=ADMIN_HOME_HREF)


@views.route('/inputs', methods=['GET', 'POST'])
@login_required
def user_input_page():
    if request.method == 'GET': 
        input_options_rows = InputOptions.query.filter_by(nursing_home_id=current_user.nursing_home_id).all()
    else:
        my_var = request.form.get('json')
        print(my_var)
        input_options_rows = InputOptions.query.filter_by(nursing_home_id=current_user.nursing_home_id).all()
    return render_template("inputs.html", user=current_user, rows=input_options_rows, home_href=ADMIN_HOME_HREF)

# ===============================================================================================================
# =============================================== Public Dashboard ==============================================
# ===============================================================================================================
@views.route('/public-dashboard', methods=['GET'])
def public_dashboard_page():
    activity=["Cycling", "Travelling", "Boating", "Write Diary", "Drinking", "Playing the piano"]
    activity_frequency=[15, 17, 9, 12, 11,15]

    activities_bar_chart = go.Figure(data=[go.Bar(x=activity, y=activity_frequency)])
    activities_bar_chart.update_layout(
                width=1500,
                height=600,
    )
    graph_activities = json.dumps(activities_bar_chart, cls=plotly.utils.PlotlyJSONEncoder)


    moods = ['happy', 'sad', 'ok']
    percentage = [35, 15, 50]
    mood_pie_chart = go.Figure(data = [go.Pie(labels = moods, values = percentage)])
    mood_pie_chart.update_layout(
                width=1500,
                height=600,
    )
    mood_ratio = json.dumps(mood_pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("public-dashboard.html",graph_activities=graph_activities, mood_ratio=mood_ratio)

# ===============================================================================================================
# ==================================================== GUEST ====================================================
# ===============================================================================================================
@views.route('/guest-inputs', methods=['GET', 'POST'])
@login_required
def guest_inputs():
    input_options_rows = InputOptions.query.filter_by(nursing_home_id=current_user.nursing_home_id).all()
    
    """ 
    Clicks on either wellbeing or activity submit button, assumes only one category submit at a time, 
    because it will ignore the other options if other category input options are chosen. 
    Eg. Happy is selected, click the activity submit button, nothing happens.
    """
    if request.method == 'POST': 
        # Empty strings returned if no options are selected
        activity_csv = request.form.get('json_activity')
        wellbeing_csv = request.form.get('json_wellbeing')
        # print(activity_csv)
        # print(wellbeing_csv)

        activity_list = activity_csv.split(',')[:-1]
        wellbeing_list = wellbeing_csv.split(',')[:-1]
        
        for activity in activity_list:          
            # user_id=0 means Guest account for the nursing home
            activity_input = Input(category="activity", name=activity, user_id=0, nursing_home_id=current_user.nursing_home_id)
            db.session.add(activity_input)
            db.session.commit()
            print(activity)
        
        for wellbeing in wellbeing_list:          
            # user_id=0 means Guest account for the nursing home
            wellbeing_input = Input(category="wellbeing", name=wellbeing, user_id=0, nursing_home_id=current_user.nursing_home_id)
            db.session.add(wellbeing_input)
            db.session.commit()
            print(wellbeing)
    
    return render_template("guest_inputs.html", user=current_user, rows=input_options_rows, name=get_name("guest"),
        home_href=GUEST_HOME_HREF)
    
@views.route('/inputs', methods=['GET', 'POST'])
@login_required
def guest_input():
    if request.method == 'GET': 
        input_options_rows = InputOptions.query.filter_by(nursing_home_id=current_user.nursing_home_id).all()
    else:
        my_var = request.form.get('json')
        print(my_var)
        input_options_rows = InputOptions.query.filter_by(nursing_home_id=current_user.nursing_home_id).all()
    return render_template("input/inputs.html", user=current_user, rows=input_options_rows, home_href=GUEST_HOME_HREF)

# ===============================================================================================================
# ================================================= RESIDENT ====================================================
# ===============================================================================================================
@views.route('/user', methods=['GET', 'POST'])
@login_required
def user_home():
    return render_template("user/home_user.html", user=current_user, name=get_name("resident"), home_href=USER_HOME_HREF)

@views.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    return render_template("user/profile_update_user.html", user=current_user, name=get_name("resident"), home_href=USER_HOME_HREF)

@views.route('/user/inputs', methods=['GET', 'POST'])
@login_required
def user_input():
    if request.method == 'GET': 
        input_options_rows = InputOptions.query.filter_by(nursing_home_id=current_user.nursing_home_id).all()
    else:
        my_var = request.form.get('json')
        print(my_var)
        input_options_rows = InputOptions.query.filter_by(nursing_home_id=current_user.nursing_home_id).all()
    return render_template("inputs.html", user=current_user, rows=input_options_rows, name=get_name("resident"), home_href=USER_HOME_HREF)