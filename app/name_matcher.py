from rapidfuzz import process, fuzz
from typing import List, Tuple

def load_names(filepath: str) -> List[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Best-match + ranked list function
def match_name(query: str, names: List[str], top_k: int = 5):
    # Use token_sort_ratio to handle reordering; fallback to ratio.
    scorer = fuzz.token_sort_ratio
    matches = process.extract(query, names, scorer=scorer, limit=top_k)
    # matches: list of (name, score, index)
    best = matches[0] if matches else (None, 0, None)
    ranked = [{"name": m[0], "score": m[1]} for m in matches]
    return {"best_match": {"name": best[0], "score": best[1]}, "ranked": ranked}
