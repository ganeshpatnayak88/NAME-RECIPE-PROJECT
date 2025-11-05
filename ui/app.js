// ui/app.js
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("nameBtn").addEventListener("click", matchName);
  document.getElementById("recipeBtn").addEventListener("click", getRecipes);
});

async function matchName() {
  const input = document.getElementById("nameInput");
  const out = document.getElementById("nameOutput");
  const q = input.value.trim();
  if (!q) { out.innerHTML = '<p class="text-red-500">Please enter a name.</p>'; return; }

  out.innerHTML = '<p class="text-gray-500">⏳ Searching...</p>';
  try {
    const res = await fetch('/match_name', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: q, top_k: 5 })
    });
    const data = await res.json();
    if (!res.ok) {
      out.innerHTML = `<p class="text-red-500">Error: ${data.detail || res.statusText}</p>`;
      return;
    }
    if (!data.best_match) {
      out.innerHTML = `<p class="text-gray-700">No matches found.</p>`;
      return;
    }
    out.innerHTML = `
      <div><strong>Best:</strong> ${escapeHtml(data.best_match.name)} (${Number(data.best_match.score).toFixed(2)}%)</div>
      <hr class="my-2">
      <div><strong>Top matches:</strong></div>
      <ul class="list-disc pl-5 mt-1">
        ${data.ranked.map(m => `<li>${escapeHtml(m.name)} (${Number(m.score).toFixed(2)}%)</li>`).join('')}
      </ul>
    `;
  } catch (err) {
    out.innerHTML = `<p class="text-red-500">Network error: ${err.message}</p>`;
  }
}

async function getRecipes() {
  const input = document.getElementById("recipeInput");
  const out = document.getElementById("recipeOutput");
  const arr = input.value.split(',').map(s => s.trim()).filter(Boolean);
  if (arr.length === 0) { out.innerHTML = '<p class="text-red-500">Please enter ingredients.</p>'; return; }

  out.innerHTML = '<p class="text-gray-500">🤖 Finding recipes...</p>';
  try {
    const res = await fetch('/recipe_chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ingredients: arr, top_k: 5 })
    });
    const data = await res.json();
    if (!res.ok) {
      out.innerHTML = `<p class="text-red-500">Error: ${data.detail || res.statusText}</p>`;
      return;
    }
    if (!data.matches || data.matches.length === 0) {
      out.innerHTML = '<p class="text-gray-700">No matching recipes found.</p>';
      return;
    }
    out.innerHTML = data.matches.map(r => `
      <div class="border rounded p-2 mb-2 bg-green-50">
        <div class="font-semibold text-green-800">🥣 ${escapeHtml(r.title)}</div>
        <div class="text-sm text-gray-700 mt-1"><b>Ingredients:</b> ${r.ingredients.map(i=>escapeHtml(i)).join(', ')}</div>
        <div class="text-sm text-gray-600 mt-1"><b>Instructions:</b> ${escapeHtml(r.instructions)}</div>
        <div class="text-xs text-gray-500 mt-1">Score: ${r.score}</div>
      </div>
    `).join('');
  } catch (err) {
    out.innerHTML = `<p class="text-red-500">Network error: ${err.message}</p>`;
  }
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
