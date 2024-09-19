from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, UserStats, WorkoutPlan
from forms import RegistrationForm, LoginForm, UserStatsForm
from flask_login import login_user, logout_user, login_required,current_user
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        
        if existing_user or existing_email:
            flash('Username or email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('main.register'))
        
        # Hash the password before storing it
        hashed_password = generate_password_hash(form.password.data)
        
        # Create a new user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        # Add and commit to the database
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)


'''@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  #an object of the register form class
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)'''

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash('Login Successful!', 'success')
            return redirect(url_for('main.stats'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', form=form)
'''@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == hashed_password:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)'''

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')




@main.route('/collect_stats', methods=['GET', 'POST'])
@login_required
def collect_stats():
    form = UserStatsForm()
    if form.validate_on_submit():
        height_total_inches = form.height_feet.data * 12 + form.height_inches.data
        stats = UserStats(
            weight=form.weight.data,
            height=height_total_inches,
            age=form.age.data,
            gender=form.gender.data,
            activity_level=form.activity_level.data,
            week=form.week.data,
            owner=current_user
        )
        db.session.add(stats)
        db.session.commit()
        flash('Stats collected successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('stats.html', form=form)



@main.route('/generate_plans', methods=['GET','POST'])
@login_required
def generate_plans():
    # Fetch user stats
    user_stats = UserStats.query.filter_by(user_id=current_user.id).first()

    if user_stats is None:
        flash('User stats not found. Please complete your stats profile.', 'danger')
        return redirect(url_for('main.collect_stats'))

    # Get the number of weeks from user stats
    num_weeks = user_stats.week
    if not num_weeks:
        flash('Number of weeks not specified in user stats.', 'danger')
        return redirect(url_for('main.collect_stats'))


    client = OpenAI()
    # Initialize an empty string to hold the full workout plan

    latest_plan_group = db.session.query(db.func.max(WorkoutPlan.plan_group)).scalar() or 0
    new_plan_group = latest_plan_group + 1 
   
    plans = []
    try:
        # Loop through the number of weeks from the database
        for week in range(1, int(num_weeks) + 1):
            prompt = (
                f"Generate a workout plan for a {user_stats.age}-year-old {user_stats.gender} "
                f"weighing {user_stats.weight} lbs and {user_stats.height} inches tall. "
                f"Activity level: {user_stats.activity_level}. Duration: Week {week}."
            )

            # OpenAI API request
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a fitness coach, skilled in coming up with weekly workout plans for your clients based on thier age, gender, weight, height, and activity level."},
                    {"role": "user", "content": prompt}
                    ]
            )

            # Extract the workout plan from the response
            workout_plan = response.choices[0].message.content

            # Concatenate the workout plan for the week to the full plan
            '''full_workout_plan += f"Week {week}:\n{workout_plan}\n\n" '''

            print(workout_plan)

            # Save the generated plan to the database
            new_plan = WorkoutPlan(
                user_id=current_user.id,
                plan=workout_plan,
                plan_group=new_plan_group
            )
            db.session.add(new_plan)
            db.session.commit()

            # Append to plans for display
            plans.append({'plan': workout_plan})

        flash('Workout plans generated successfully', 'success')
        return redirect(url_for('main.plan'))
    except Exception as e:
        flash(f"An error occurred while generating the workout plan: {e}", 'danger')
        return redirect(url_for('main.home'))



'''@main.route('/generate_plans', methods=['GET','POST'])
@login_required
def generate_plans():
    user_stats = UserStats.query.filter_by(user_id=current_user.id).first()

    if user_stats is None:
        flash('User stats not found. Please complete your stats profile.', 'danger')
        return redirect(url_for('main.collect_stats'))

    OpenAI.api_key = os.environ.get('OPENAI_API_KEY')

    plans = []
    for week in range(1, int(request.form['week']) + 1):
        prompt = (
            f"Generate a workout plan for a {user_stats.age}-year-old {user_stats.gender} "
            f"weighing {user_stats.weight} lbs and {user_stats.height} inches tall. "
            f"Activity level: {user_stats.activity_level}. Duration: Week {week}."
        )

        try:
            response = OpenAI.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )
            workout_plan = response['choices'][0]['message']['content']

            new_plan = WorkoutPlan(
                user_id=current_user.id,
                week=week,
                plan=workout_plan
            )
            db.session.add(new_plan)
            db.session.commit()

            plans.append({'week': week, 'plan': workout_plan})
        except Exception as e:
            flash(f"An error occurred while generating the workout plan: {e}", 'danger')
            return redirect(url_for('main.plan'))

    flash('Workout plans generated successfully', 'success')
    return render_template('plans.html', plans=plans)


#
@main.route('/generate_plans', methods=['GET','POST'])
@login_required
def generate_plans():
    user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
    
    if user_stats is None:
        flash('User stats not found. Please complete your stats profile.', 'danger')
        return redirect(url_for('main.collect_stats'))

   
    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY')
    )

    plans = []
    for week in range(1, int(request.form['weeks']) + 1):
        prompt = (
            f"Generate a workout plan for a {user_stats.age}-year-old {user_stats.gender} "
            f"weighing {user_stats.weight} lbs and {user_stats.height} inches tall. "
            f"Activity level: {user_stats.activity_level}. Duration: Week {week}."
        )

        try:
            response = client.chat.completions.create(
                engine="gpt-3.5-turbo",
                messages=prompt,
                max_tokens=1024
            )
            workout_plan = response.choices[0].message
            plans.append({'week': week, 'plan': workout_plan})
        except Exception as e:
            flash(f"An error occurred while generating the workout plan: {e}", 'danger')
            return redirect(url_for('main.plan'))

    flash('Workout plans generated successfully', 'success')
    return render_template('plans.html', plans=plans)


@main.route('/generate_plan', methods=['POST'])
@login_required
def generate_plan():
    user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
    
    if user_stats is None:
        flash('User stats not found. Please complete your stats profile.', 'danger')
        return redirect(url_for('main.collect_stats'))  # Redirect to a page where the user can complete their stats

    openai.api_key = os.environ.get('OPENAI_API_KEY')

    prompt = (
        f"Generate a workout plan for a {user_stats.age}-year-old {user_stats.gender} "
        f"weighing {user_stats.weight} lbs and {user_stats.height} inches tall. "
        f"Activity level: {user_stats.activity_level}. Duration: {request.form['weeks']} weeks."
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024
        )
        workout_plan = response.choices[0].text
    except Exception as e:
        flash(f"An error occurred while generating the workout plan: {e}", 'danger')
       
    flash('Workout plan generated successfully', 'success')
    return redirect(url_for('main.plan')) 



@main.route('/generate_plan', methods=['POST'])
@login_required
def generate_plan():
    user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    prompt = (
        f"Generate a workout plan for a {user_stats.age}-year-old {user_stats.gender} "
        f"weighing {user_stats.weight} lbs and {user_stats.height} inches tall. "
        f"Activity level: {user_stats.activity_level}. Duration: {request.form['weeks']} weeks."
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024
    )

    workout_plan = response.choices[0].text

    flash('Workout plan generated successfully', 'success')
    return render_template('plan.html', plan=workout_plan)'''

@main.route('/plan')
@login_required
def plan():
    latest_plan_group = db.session.query(db.func.max(WorkoutPlan.plan_group)).filter_by(user_id=current_user.id).scalar()
    if latest_plan_group is None:
        flash('No workout plans available.', 'danger')
        return redirect(url_for('main.home'))


    recent_plans = WorkoutPlan.query.filter_by(user_id=current_user.id, plan_group=latest_plan_group).order_by(WorkoutPlan.id.desc()).all()
    
    return render_template('plan.html', plan=recent_plans)
  

'''@main.route('/create')
@login_required
def create():
    return render_template('create.html')

@main.route('/save_plan', methods=['POST'])
@login_required
def save_plan():
    plan = WorkoutPlan(user_id=current_user.id, plan=request.form['plan'])
    db.session.add(plan)
    db.session.commit()
    flash('Workout plan saved successfully', 'success')
    return redirect(url_for('main.dashboard'))
'''

@main.route('/view_plans')
@login_required
def view_plans():
    plans = WorkoutPlan.query.filter_by(user_id=current_user.id).all()
    return render_template('view_plans.html', plans=plans)
