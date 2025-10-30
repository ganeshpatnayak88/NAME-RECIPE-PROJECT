# 🍳 Name & Recipe Matching API

### Assignment Submission by: **Ganesh (MP Ganesh)**

---

## 🧭 Project Overview

This project implements **two main tasks** as per the company’s hiring assignment:

### 🧩 Task 1 – Name Matching API
- Accepts an input name (query).
- Returns the **best matching name** and a **ranked list** with similarity scores.
- Uses **RapidFuzz** for fast and accurate fuzzy string matching.
- Handles spelling differences and partial matches efficiently.

### 🍲 Task 2 – Recipe Chatbot API
- Accepts a list of ingredients as input.
- Returns the most relevant **recipes** that can be made with those ingredients.
- Provides both structured JSON and a **chatbot-style response** (human-readable text).
- Uses lightweight retrieval logic based on ingredient overlap (no GPU or heavy model needed).

---

## 📂 Project Structure

name-recipe-project/
├─ app/
│ ├─ main.py # FastAPI server & endpoints
│ ├─ name_matcher.py # Task 1: Name similarity logic
│ └─ recipe_engine.py # Task 2: Recipe search logic
├─ data/
│ ├─ names_list.txt # List of sample names (30+ entries)
│ └─ recipes.json # Small recipe dataset
├─ ui/
│ ├─ index.html # Simple frontend UI
│ └─ app.js # JavaScript for calling APIs
├─ requirements.txt # Python dependencies
└─ README.md # Project documentation (this file)



---

## ⚙️ Installation & Setup

### 1️⃣ Create and activate a virtual environment

Open PowerShell in the project folder:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1

If you see an “execution policy” error:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

2️⃣ Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

Or manually install:
pip install fastapi uvicorn[standard] rapidfuzz pydantic python-multipart jinja2 aiofiles


3️⃣ Run the server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

You’ll see:
Uvicorn running on http://127.0.0.1:8000


🧪 API Endpoints
✅ 1. POST /match_name
Description: Finds the closest matching names and similarity scores.
Sample Request:
{
  "query": "Geetha",
  "top_k": 5
}

Sample Response:
{
  "best_match": {
    "name": "Geetha",
    "score": 100.0
  },
  "ranked": [
    {"name": "Geetha", "score": 100.0},
    {"name": "Geeta", "score": 90.9},
    {"name": "Getha", "score": 90.9},
    {"name": "Geesha", "score": 83.3}
  ]
}


✅ 2. POST /recipe_chat
Description: Suggests recipes based on a list of ingredients.
Sample Request:
{
  "ingredients": ["egg", "onion"],
  "top_k": 3
}

Sample Response:
{
  "matches": [
    {
      "id": 1,
      "title": "Egg & Onion Scramble",
      "score": 2,
      "ingredients": ["egg", "onion", "salt", "pepper", "oil"],
      "instructions": "Beat eggs, chop onions, fry onions, add eggs, scramble. Serve."
    },
    {
      "id": 2,
      "title": "Onion Omelette",
      "score": 2,
      "ingredients": ["egg", "onion", "salt", "butter"],
      "instructions": "Whisk eggs with salt. Sauté onions in butter. Pour eggs, cook till done."
    }
  ],
  "response_text": "Try 'Egg & Onion Scramble' (match score 2):\nIngredients: egg, onion, salt, pepper, oil\nSteps: Beat eggs, chop onions, fry onions, add eggs, scramble. Serve.\n\nTry 'Onion Omelette' (match score 2):\nIngredients: egg, onion, salt, butter\nSteps: Whisk eggs with salt. Sauté onions in butter. Pour eggs, cook till done."
}


🌐 Testing the API
Option 1 — Thunder Client (VS Code)


Open the Thunder Client tab (⚡ icon).


Create a new request:


Method: POST


URL: http://127.0.0.1:8000/match_name


Body (JSON):
{"query": "Geetha", "top_k": 5}





Send the request and check the response.


Repeat for /recipe_chat.

Option 2 — FastAPI Swagger UI
Open in browser:
👉 http://127.0.0.1:8000/docs
You can interactively test both endpoints here.

📊 Dataset Description
names_list.txt


Contains over 30+ names (variations like Gita, Geeta, Geetha, Githa, etc.)


Used to test name matching performance.


recipes.json


Small dataset of recipes.


Each record includes:


id: unique ID


title: recipe name


ingredients: list of ingredients


instructions: preparation steps




You can easily extend it with more recipes from open datasets (like Kaggle or RecipeNLG).

🚀 How It Works
🔹 Name Matching


Uses RapidFuzz’s token_sort_ratio scorer.


Compares the input with all names in the dataset.


Returns top K most similar names and their scores (0–100).


🔹 Recipe Chatbot


Matches recipes by overlapping ingredients.


Higher overlap → higher relevance score.


Returns both structured recipe details and human-friendly message text.



🧩 Optional Enhancements


Integrate a small local LLM (e.g., distilgpt2 or TinyLLaMA) for natural language recipe generation.


Use Sentence Transformers and FAISS for vector-based ingredient matching.


Expand recipe dataset for better coverage.



✅ Verification Checklist
FeatureStatus/match_name working✅/recipe_chat working✅FastAPI server runs successfully✅Tested via Thunder Client✅Datasets properly loaded✅JSON responses formatted & correct✅

🏁 How to Stop the Server
Press CTRL + C in the terminal window where Uvicorn is running.

👨‍💻 Author
Ganesh (MP Ganesh)
Python Developer | AI Enthusiast


