from rapidfuzz import process, fuzz

def load_names(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def match_name(query, names, top_k=5):
    # Use token_sort_ratio to be robust to token order changes
    matches = process.extract(query, names, scorer=fuzz.token_sort_ratio, limit=top_k)
    if not matches:
        return {"best_match": None, "ranked": []}
    ranked = [{"name": m[0], "score": float(m[1])} for m in matches]
    return {"best_match": ranked[0], "ranked": ranked}
