const API_BASE = "http://localhost:8000";

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const previewContainer = document.getElementById("preview-container");
const previewImg = document.getElementById("preview-img");
const analyzeBtn = document.getElementById("analyze-btn");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error-box");
const results = document.getElementById("results");
const resetBtn = document.getElementById("reset-btn");

let selectedFile = null;

// ── File selection ──────────────────────────────────────────────────────────

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) handleFileSelected(file);
});

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) handleFileSelected(fileInput.files[0]);
});

function handleFileSelected(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewContainer.style.display = "block";
    analyzeBtn.style.display = "block";
    hideError();
    results.style.display = "none";
  };
  reader.readAsDataURL(file);
}

// ── Analyze ─────────────────────────────────────────────────────────────────

analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  setLoading(true);
  hideError();
  results.style.display = "none";

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const response = await fetch(`${API_BASE}/analyze-room`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong.");
    }

    renderResults(data);
  } catch (err) {
    showError(err.message || "Could not reach the server. Make sure the backend is running.");
  } finally {
    setLoading(false);
  }
});

// ── Render results ───────────────────────────────────────────────────────────

function renderResults(data) {
  // Style card
  document.getElementById("res-style").textContent = data.detected_style || "—";
  document.getElementById("res-room-type").textContent = data.room_type || "—";

  const colorsEl = document.getElementById("res-colors");
  colorsEl.innerHTML = "";
  (data.color_palette || []).forEach((color) => {
    const chip = document.createElement("span");
    chip.className = "color-chip";
    chip.textContent = color;
    colorsEl.appendChild(chip);
  });

  // Product cards
  const grid = document.getElementById("product-grid");
  grid.innerHTML = "";
  (data.recommendations || []).forEach((p) => {
    grid.appendChild(buildProductCard(p));
  });

  // Total
  document.getElementById("res-total").textContent = formatUSD(data.total_landed_cost_usd);

  results.style.display = "block";
  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

function buildProductCard(p) {
  const card = document.createElement("div");
  card.className = "product-card";
  card.innerHTML = `
    <div class="product-name">${p.name}</div>
    <div class="product-category">${p.category}</div>
    <div class="product-row"><span>Origin</span><span>${flagEmoji(p.origin_country)} ${p.origin_country}</span></div>
    <div class="product-row"><span>HS Code</span><span>${p.hs_code}</span></div>
    <div class="product-row"><span>Unit Cost</span><span>${formatUSD(p.unit_cost_usd)}</span></div>
    <div class="product-row"><span>Duty (${p.duty_rate_pct}%)</span><span>+ ${formatUSD(p.duty_amount_usd)}</span></div>
    <div class="product-row"><span>Freight</span><span>+ ${formatUSD(p.freight_usd)}</span></div>
    <div class="landed-cost-row"><span>Landed Cost</span><span>${formatUSD(p.landed_cost_usd)}</span></div>
  `;
  return card;
}

// ── Reset ────────────────────────────────────────────────────────────────────

resetBtn.addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  previewContainer.style.display = "none";
  analyzeBtn.style.display = "none";
  results.style.display = "none";
  hideError();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

// ── Helpers ──────────────────────────────────────────────────────────────────

function setLoading(on) {
  loading.style.display = on ? "flex" : "none";
  analyzeBtn.disabled = on;
  analyzeBtn.textContent = on ? "Analyzing…" : "✨ Analyze Room";
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.style.display = "block";
}

function hideError() {
  errorBox.style.display = "none";
  errorBox.textContent = "";
}

function formatUSD(amount) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(amount);
}

// Country code → flag emoji
const COUNTRY_FLAGS = {
  "China": "🇨🇳", "Vietnam": "🇻🇳", "India": "🇮🇳", "Indonesia": "🇮🇩",
  "Mexico": "🇲🇽", "Poland": "🇵🇱", "Portugal": "🇵🇹", "Italy": "🇮🇹",
  "Malaysia": "🇲🇾", "United Kingdom": "🇬🇧", "New Zealand": "🇳🇿", "Turkey": "🇹🇷",
};

function flagEmoji(country) {
  return COUNTRY_FLAGS[country] || "🌍";
}
