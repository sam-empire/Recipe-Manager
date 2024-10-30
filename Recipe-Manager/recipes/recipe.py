from flask import Blueprint, render_template, redirect

recipe_bp = Blueprint("recipe", __name__, template_folder= "templates")

@recipe_bp.route('/show_recipes')
def show_recipes():
    return render_template('recipes.html')
