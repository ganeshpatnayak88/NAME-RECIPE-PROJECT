import json

def load_recipes(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ingredients_score(input_ings, recipe_ings):
    input_set = {i.lower().strip() for i in input_ings}
    recipe_set = {i.lower().strip() for i in recipe_ings}
    return len(input_set & recipe_set)

def find_best_recipes_by_ingredients(input_ingredients, recipes, top_k=3):
    scored = [(ingredients_score(input_ingredients, r.get("ingredients", [])), r) for r in recipes]
    scored = sorted(scored, key=lambda x: (-x[0], x[1].get("title", "")))
    results = []
    for s, r in scored:
        if s <= 0:
            continue
        results.append({
            "id": r.get("id"),
            "title": r.get("title"),
            "score": int(s),
            "ingredients": r.get("ingredients", []),
            "instructions": r.get("instructions", "")
        })
        if len(results) >= top_k:
            break
    return results

def format_recipe_suggestion(recipe):
    return (
        f"Try '{recipe['title']}' (match score {recipe['score']}):\n"
        f"Ingredients: {', '.join(recipe['ingredients'])}\n"
        f"Steps: {recipe['instructions']}"
    )
