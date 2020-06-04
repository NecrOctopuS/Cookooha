from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

users_recipes_association = db.Table(
    "users_recipes",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id")),
)

recipes_ingredients_association = db.Table(
    "recipes_ingredients",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id")),
    db.Column("ingredient_id", db.Integer, db.ForeignKey("ingredients.id")),
)


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    description = db.Column(db.String(2000))
    time = db.Column(db.Integer)  # время приготовления в минутах
    servings = db.Column(db.Integer)  # кол-во порций
    kcal = db.Column(db.Integer)
    instruction = db.Column(db.String(2000))
    ingredients = db.relationship("Ingredient", secondary=recipes_ingredients_association, back_populates="recipes")
    users = db.relationship("User", secondary=users_recipes_association, back_populates="favorites")


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    ingredient_group_id = db.Column(db.Integer, db.ForeignKey('ingredient_groups.id'))
    ingredient_group = db.relationship("IngredientGroup")
    recipes = db.relationship("Recipe", secondary=recipes_ingredients_association, back_populates="ingredients")


class IngredientGroup(db.Model):
    __tablename__ = "ingredient_groups"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    ingredients = db.relationship("Ingredient")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    favorites = db.relationship("Recipe", secondary=users_recipes_association, back_populates="users")

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)
