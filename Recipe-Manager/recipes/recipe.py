from flask import Blueprint, render_template, redirect

recipe_bp = Blueprint("recipe", __name__, template_folder= "templates")
from database import get_db_connection


@recipe_bp.route('/show_recipes')
def show_recipes():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('recipes.html', recipes=recipes)


