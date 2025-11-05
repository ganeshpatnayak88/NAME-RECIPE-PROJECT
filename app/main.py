import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

from app.name_matcher import load_names, match_name
from app.recipe_engine import load_recipes, find_best_recipes_by_ingredients, format_recipe_suggestion

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = os.path.join(BASE_DIR, "ui")
DATA_DIR = os.path.join(BASE_DIR, "data")
NAMES_FILE = os.path.join(DATA_DIR, "names_list.txt")
RECIPES_FILE = os.path.join(DATA_DIR, "recipes.json")

app = FastAPI(title="Name & Recipe Service")

# Serve static assets (JS/CSS) at /static -> prevents overlapping with API routes
app.mount("/static", StaticFiles(directory=UI_DIR), name="static")

# Serve index.html explicitly at '/'
@app.get("/", include_in_schema=False)
def index():
    index_path = os.path.join(UI_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=500, detail="index.html not found on server")
    return FileResponse(index_path, media_type="text/html")

# Load datasets at startup (simple, in-memory; fine for demo)
names = load_names(NAMES_FILE)
recipes = load_recipes(RECIPES_FILE)

# Request models
class NameQuery(BaseModel):
    query: str
    top_k: int = 5

class IngredientQuery(BaseModel):
    ingredients: List[str]
    top_k: int = 3

# API endpoints
@app.post("/match_name")
def api_match_name(q: NameQuery):
    res = match_name(q.query, names, top_k=q.top_k)
    return res

@app.post("/recipe_chat")
def api_recipe_chat(q: IngredientQuery):
    matches = find_best_recipes_by_ingredients(q.ingredients, recipes, top_k=q.top_k)
    if not matches:
        raise HTTPException(status_code=404, detail="No recipes found")
    conv = "\n\n".join(format_recipe_suggestion(m) for m in matches)
    return {"matches": matches, "response_text": conv}
