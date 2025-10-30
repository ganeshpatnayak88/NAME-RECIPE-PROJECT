async function matchName(){
  const q = document.getElementById("nameInput").value;
  const res = await fetch("/match_name", {
    method:"POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({query: q, top_k:5})
  });
  const data = await res.json();
  document.getElementById("nameResult").textContent = JSON.stringify(data, null, 2);
}

async function findRecipe(){
  const ings = document.getElementById("ingredientsInput").value.split(",").map(s=>s.trim()).filter(Boolean);
  const res = await fetch("/recipe_chat", {
    method:"POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ingredients: ings, top_k:3})
  });
  const data = await res.json();
  document.getElementById("recipeResult").textContent = data.response_text || JSON.stringify(data, null, 2);
}
