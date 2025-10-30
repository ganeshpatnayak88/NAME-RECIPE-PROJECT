import json
from typing import List, Dict

def load_recipes(path="data/recipes.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_ingredient(ing: str) -> str:
    return ing.lower().strip()

def ingredients_score(query_ings: List[str], recipe_ings: List[str]) -> int:
    qset = set(normalize_ingredient(i) for i in query_ings)
    rset = set(normalize_ingredient(i) for i in recipe_ings)
    overlap = qset & rset
    return len(overlap)

def find_best_recipes_by_ingredients(input_ingredients: List[str], recipes: List[Dict], top_k=3):
    scored = []
    for r in recipes:
        score = ingredients_score(input_ingredients, r.get("ingredients", []))
        scored.append((score, r))
    scored = sorted(scored, key=lambda x: (-x[0], x[1]["title"]))
    results = [
        {
            "id": r["id"],
            "title": r["title"],
            "score": s,
            "ingredients": r["ingredients"],
            "instructions": r["instructions"],
        }
        for s, r in scored
        if s > 0
    ][:top_k]

    if not results:
        # fallback: return top few anyway
        for s, r in scored[:top_k]:
            results.append({
                "id": r["id"],
                "title": r["title"],
                "score": s,
                "ingredients": r["ingredients"],
                "instructions": r["instructions"],
            })
    return results

def format_recipe_suggestion(recipe):
    """Create a friendly text for chatbot response."""
    return (
        f"Try '{recipe['title']}' (match score {recipe['score']}):\n"
        f"Ingredients: {', '.join(recipe['ingredients'])}\n"
        f"Steps: {recipe['instructions']}"
    )
