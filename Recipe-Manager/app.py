from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import os

from recipes import recipe_bp
app = Flask(__name__)

# Register blueprints
app.register_blueprint(recipe_bp, url_prefix='/recipe')

# Basic configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/meal_planner')
def meal_planner():
    return render_template('meal_planner.html')

@app.route('/favorites')
def show_favorites():  
    return render_template('favourites.html')

if __name__ == '__main__':
    app.run(debug=True)
