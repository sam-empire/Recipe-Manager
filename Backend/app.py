from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import os

app = Flask(__name__)

# Basic configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking for performance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev_db.sqlite3')

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_recipes')
def show_recipes():
    return render_template('show_recipes.html')

@app.route('/meal_planner')
def meal_planner():
    return render_template('meal_planner.html')

@app.route('/favorites')
def show_favorites():  
    return render_template('favourites.html')

if __name__ == '__main__':
    app.run(debug=True)
