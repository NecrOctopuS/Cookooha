import json
from app.models import Recipe, Ingredient, IngredientGroup
from app import app, db


def read_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        contents = file.read()
    if contents:
        return json.loads(contents)
    return []


def add_ingredients(json_path):
    ingredients = read_json(json_path)
    for data in ingredients:
        ingredient = Ingredient(id=data['id'],
                                title=data['title'],
                                ingredient_group_id=data['ingredient_group'])
        db.session.add(ingredient)
    db.session.commit()


def add_ingredient_groups(json_path):
    ingredient_groups = read_json(json_path)
    for data in ingredient_groups:
        ingredient_group = IngredientGroup(
            id=data['id'],
            title=data['title'],
        )
        db.session.add(ingredient_group)
    db.session.commit()


def add_recipes(json_path):
    recipes = read_json(json_path)
    for data in recipes:
        recipe = Recipe(
            id=data['id'],
            title=data['title'],
            picture=data['picture'],
            description=data['description'],
            time=data['time'],
            servings=data['servings'],
            kcal=data['kcal'],
            instruction=data['instruction']
        )
        ingredients = data['ingredients']
        for ingredient_id in ingredients:
            ingredient = db.session.query(Ingredient).get(ingredient_id)
            recipe.ingredients.append(ingredient)
        db.session.add(recipe)
    db.session.commit()


def main():
    with app.app_context():
        add_ingredient_groups('ingredient_groups.json')
        add_ingredients('ingredients.json')
        add_recipes('recipes.json')


if __name__ == '__main__':
    main()
