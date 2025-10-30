from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from app.name_matcher import load_names, match_name
from app.recipe_engine import load_recipes, find_best_recipes_by_ingredients, format_recipe_suggestion

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
NAMES_FILE = os.path.join(BASE_DIR, "data", "names_list.txt")
RECIPES_FILE = os.path.join(BASE_DIR, "data", "recipes.json")

app = FastAPI(title="Name & Recipe Service")

names = load_names(NAMES_FILE)
recipes = load_recipes(RECIPES_FILE)

class NameQuery(BaseModel):
    query: str
    top_k: int = 5

class IngredientQuery(BaseModel):
    ingredients: List[str]
    top_k: int = 3

@app.post("/match_name")
def api_match_name(q: NameQuery):
    res = match_name(q.query, names, top_k=q.top_k)
    return res

@app.post("/recipe_chat")
def api_recipe_chat(q: IngredientQuery):
    matches = find_best_recipes_by_ingredients(q.ingredients, recipes, top_k=q.top_k)
    if not matches:
        raise HTTPException(status_code=404, detail="No recipes found")
    # return both structured matches and a conversational suggestion
    conv = "\n\n".join(format_recipe_suggestion(m) for m in matches)
    return {"matches": matches, "response_text": conv}
