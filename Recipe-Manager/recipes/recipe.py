from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os
from database import get_db_connection

recipe_bp = Blueprint("recipe", __name__, template_folder="templates")

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@recipe_bp.route('/show_recipes', methods=['GET', 'POST'])
def show_recipes():
    search_query = request.args.get('search', '').strip()  # Get search input
    conn = get_db_connection()

    # If a search query is provided, filter recipes by title or category
    if search_query:
        query = 'SELECT * FROM recipes WHERE category LIKE ? OR title LIKE ?'
        recipes = conn.execute(query, (f'%{search_query}%', f'%{search_query}%')).fetchall()
    else:
        # Otherwise, retrieve all recipes
        query = 'SELECT * FROM recipes'
        recipes = conn.execute(query).fetchall()

    # Convert each recipe to dictionary format
    recipes = [dict(recipe) for recipe in recipes]
    conn.close()

    return render_template('recipes.html', recipes=recipes, search_query=search_query)


@recipe_bp.route('/add_recipes', methods=('GET', 'POST'))
def add_recipes():
    if request.method == "POST":
        instructions = request.form.get('instructions')
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        category = request.form.get('category')
        image = request.files.get('recipe_image')

        ingredients = request.form.getlist('ingredients')  
        ingredients_string = ','.join(ingredients) 
        # Check if the file is an image and allowed
        if image and allowed_file(image.filename):
            # Secure the filename and save it to the upload folder
            filename = secure_filename(image.filename)
            filepath = os.path.join('static/uploads', filename)
            image.save(filepath)
            image_url = filename

        conn = get_db_connection()
        try:
            # Insert operations
            conn.execute('INSERT INTO recipes (title, instructions, ingredients, image_url, category) VALUES (?, ?, ?, ?, ?)',
                         (title, instructions, ingredients_string, image_url, category))
            conn.commit()
            print("Recipe added:", title)
        except Exception as e:
            print(f"Error when adding recipe: {e}")
        finally:
            conn.close()

        return redirect('/recipe/show_recipes')
    return render_template('add_recipe.html')

@recipe_bp.route('/view_recipe/<int:id>', methods =('POST', 'GET'))
def view_recipe(id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('view_recipe.html', recipe=recipe)

@recipe_bp.route('/edit_recipe/<int:id>', methods =('POST', 'GET'))
def edit_recipe(id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit_recipe.html', recipe=recipe)

@recipe_bp.route('/delete_recipe/<int:id>', methods =('POST', 'GET'))
def delete_recipe(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM recipes WHERE id = ?', (id,)).fetchone()
    conn.commit()
    conn.close()
    return redirect('/recipe/show_recipes')

@recipe_bp.route('/update_recipe', methods = ('POST', 'GET'))
def update_recipe():
    if request.method == 'POST':
        recipe_id = request.form.get('recipe_id')
        instructions = request.form.get('instructions')
        ingredients = request.form.get('ingredients')
        title = request.form.get('title')
        category = request.form.get('category')
        conn = get_db_connection()
        conn.execute('UPDATE recipes SET instructions = ?, ingredients = ?, category = ?, title = ? WHERE id = ?', (instructions, ingredients, category, title, recipe_id))
        conn.commit()
        conn.close()
        return redirect('/recipe/show_recipes')
    return redirect('/recipe/show_recipes')