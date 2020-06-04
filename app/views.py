from flask import render_template, request, session, redirect, url_for, flash
from functools import wraps
from sqlalchemy import func
from app import app, db
from app.models import User, Recipe, Ingredient, IngredientGroup, users_recipes_association, \
    recipes_ingredients_association
from app.forms import RegistrationForm, LoginForm
from app.config import Config


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def get_user_from_session_or_none():
    user_id = session.get('user_id')
    if user_id:
        return db.session.query(User).get(user_id)
    return None


@app.route('/')
def render_main():
    user = get_user_from_session_or_none()
    # This query equal to
    # SELECT recipes.*  FROM recipes
    # LEFT JOIN users_recipes on recipes.id = users_recipes.recipe_id
    # LEFT JOIN users on users_recipes.user_id = users.id
    # GROUP BY recipes.id
    # ORDER BY count(users.id) DESC
    query = db.session.query(Recipe)
    query = query.join(users_recipes_association, Recipe.id == users_recipes_association.c.recipe_id, isouter=True)
    query = query.join(User, users_recipes_association.c.user_id == User.id, isouter=True)
    recipes = query.group_by(Recipe.id).order_by(func.count(User.id).desc()).limit(Config.RECIPES_PER_MAIN_PAGE)
    return render_template('index.html', user=user, recipes=recipes)


@app.route('/wizard/')
def render_wizard():
    user = get_user_from_session_or_none()
    ingredient_groups = db.session.query(IngredientGroup).all()
    selected_ingredients = session.get('selected_ingredients')
    return render_template('list.html', user=user, groups=ingredient_groups, selected_ingredients=selected_ingredients)


@app.route('/wizard-results/', methods=["GET", "POST"])
def render_wizard_results():
    user = get_user_from_session_or_none()
    if request.method == "POST":
        selected_ingredients = request.form.getlist("ingredients")
        session['selected_ingredients'] = selected_ingredients
    # This query equal to
    # SELECT recipes.*
    # FROM recipes LEFT JOIN recipes_ingredients ON recipes.id = recipes_ingredients.recipe_id
    # LEFT JOIN ingredients ON recipes_ingredients.ingredient_id = ingredients.id
    # WHERE ingredient_id IN (selected_ingredients)
    # GROUP BY recipes.title
    # ORDER BY count(recipes.title) DESC
    query = db.session.query(Recipe)
    query = query.join(recipes_ingredients_association, Recipe.id == recipes_ingredients_association.c.recipe_id)
    query = query.join(Ingredient, Ingredient.id == recipes_ingredients_association.c.ingredient_id)
    recipes = query.filter(Ingredient.id.in_((session['selected_ingredients']))). \
        group_by(Recipe.id).order_by(func.count(Recipe.title).desc()).all()
    return render_template('recipes.html', user=user, recipes=recipes)


@app.route('/recipe/<int:recipe_id>/')
def render_recipe(recipe_id):
    recipe = db.session.query(Recipe).get_or_404(recipe_id)
    instruction = recipe.instruction.replace('   ', '\n\n')
    user = get_user_from_session_or_none()
    selected_ingredients = session.get('selected_ingredients')
    return render_template('recipe.html',
                           recipe=recipe,
                           instruction=instruction,
                           user=user,
                           selected_ingredients=selected_ingredients)


@app.route('/recipe/<int:recipe_id>/add_to_favorites/')
@login_required
def add_to_favorites(recipe_id):
    user = get_user_from_session_or_none()
    recipe = db.session.query(Recipe).get_or_404(recipe_id)
    user.favorites.append(recipe)
    db.session.commit()
    flash('Блюдо добавлено в избранное.')
    return redirect(url_for('render_favorites'))


@app.route('/favorites/')
@login_required
def render_favorites():
    user = get_user_from_session_or_none()
    return render_template('fav.html', user=user, recipes=user.favorites)


@app.route('/favorites/<int:recipe_id>/')
@login_required
def delete_favorite(recipe_id):
    user = get_user_from_session_or_none()
    recipe = db.session.query(Recipe).get_or_404(recipe_id)
    user.favorites.remove(recipe)
    db.session.commit()
    flash('Блюдо удалено из избранного.')
    return redirect(url_for('render_favorites'))


@app.route('/login/', methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for('render_main'))
    form = LoginForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("login.html", form=form)
        user = User.query.filter(User.username == form.email.data).first()
        if user and user.password_valid(form.password.data):
            session["user_id"] = user.id
            return redirect(url_for('render_main'))
        form.email.errors.append("Неверное имя или пароль")
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    session.pop("user_id")
    return redirect(url_for('render_main'))


@app.route('/register/', methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for('render_main'))
    form = RegistrationForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("register.html", form=form)
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if email and password and password == confirm_password:
            user = User(username=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        elif not email or not password:
            form.email.errors.append("Не указано имя или пароль")
        elif password != confirm_password:
            form.confirm_password.errors.append("Введенные пароли не совпадают")
    return render_template("register.html", form=form)
