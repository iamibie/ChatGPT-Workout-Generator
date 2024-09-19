# Flask Workout Generator with OpenAI API

This is a web application that generates personalized workout plans based on user stats such as weight, height, age, gender, activity level, and the number of weeks for the plan. The app is built with Flask, SQLAlchemy, and Flask-WTF, and uses the OpenAI API to generate the workout plans.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Routes](#routes)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and login
- Collects user stats for workout generation
- Generates a personalized workout plan using OpenAI API
- Displays and saves generated workout plans to the database
- Secure user authentication using Flask-Login
- Fully responsive design with Bootstrap
- Persistent data storage using SQLite or PostgreSQL

## Technologies Used
- Backend: Python, Flask, Flask-WTF, SQLAlchemy, Flask-Login
- Frontend: HTML5, CSS3, Bootstrap, Jinja
- APIs: OpenAI API for workout plan generation
- Database: SQLite (or PostgreSQL in production)
- Deployment: Can be deployed on platforms like Heroku, AWS, or PythonAnywhere



## Project Structure

workout-app/
│
├── instance
├── migration
├── venv/  (your virtual environment)
├── static/
│   ├── img
│   ├── script.js
│   ├── styles.css
├── templates/
│   ├── about.html
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── plan.html
│   ├── register.html
│   ├── stats.html
│   └── view_plans.html
├── env
├── .gitignore
├── app.py
├── config.py
├── forms.py
├── models.py
├── README.md
├── requirements.txt
├── routes.py
└── run.py

## Setup Instructions
Prerequisites
  - Python 3.x
  - Virtual environment (optional, but recommended)
  - OpenAI API key (required for generating workout plans)

Step-by-Step Guide
1. Clone the repository:
  ```bash
    git clone https://github.com/your-username/this-repo.git
    cd workout-app

2. Set up a virtual environment (optional, but recommended):
    python3 -m venv venv
    source venv/bin/activate  #On Windows: venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Configure your environment variables:
   Create a .env file in the root directory of the project and add the following variables:
   OPENAI_API_KEY=your-openai-api-key
   SECRET_KEY=your-secret-key
   SQLALCHEMY_DATABASE_URI=sqlite:///workout_app.db  # Or use PostgreSQL for production

5. Set up the database:
    flask db init
    flask db migrate
    flask db upgrade

6. Run the application:

## Usage
User Registration and Login
- Users can sign up by providing their username, email, and password.
- After registration, they can log in to the app.
Generating a Workout Plan
- After logging in, users can enter their stats (weight, height, age, etc.) and specify the number of weeks for the workout plan.
- The app uses the OpenAI API to generate a workout plan and displays it.
- Users can save the generated workout plan to the database.
Viewing Saved Plans
- Users can view all their previously saved workout plans under the "Plans" section.

## Routes
Route	          Method	          Description
/register	      GET, POST	        Register a new user
/login	        GET, POST	        Log in an existing user
/collect_stats	GET, POST	        Collect user stats for workout generation
/generate_plan	POST	            Generate workout plan based on user stats
/view_plans	    GET	              View all saved workout plans
/logout	        GET	              Log out the current user



## Screenshots
Registration Page

Collect Stats Page

Generated Workout Plan Page

## Contributing
- Fork the repository.
-cCreate a new branch (git checkout -b feature-branch).
-cMake your changes.
- Commit your changes (git commit -m 'Add new feature').
- Push to the branch (git push origin feature-branch).
- Open a pull request.


## License
- This project is licensed under the MIT License. See the LICENSE file for more information.
