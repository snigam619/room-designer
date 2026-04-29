const API_BASE = "http://localhost:8000";

// ── State ─────────────────────────────────────────────────────────────────────
let state = {
  file: null,
  style: "modern",
  mood: "light",
  budget: "1000",
  design: null,
  selectedWallColor: null,
  selectedDecorId: null,
  selectedDecorCost: 0,
  selectedProducts: {},
};

// ── DOM refs ──────────────────────────────────────────────────────────────────
const stepUpload  = document.getElementById("step-upload");
const stepPrefs   = document.getElementById("step-prefs");
const dropZone    = document.getElementById("drop-zone");
const fileInput   = document.getElementById("file-input");
const previewWrap = document.getElementById("preview-wrap");
const previewImg  = document.getElementById("preview-img");
const nextBtn     = document.getElementById("next-btn");
const backBtn     = document.getElementById("back-btn");
const designBtn   = document.getElementById("design-btn");
const loading     = document.getElementById("loading");
const errorBox    = document.getElementById("error-box");
const results     = document.getElementById("results");
const resetBtn    = document.getElementById("reset-btn");

// ── Tab switching ─────────────────────────────────────────────────────────────
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
  });
});

// ── File upload ───────────────────────────────────────────────────────────────
dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener("change", () => { if (fileInput.files[0]) handleFile(fileInput.files[0]); });

function handleFile(file) {
  state.file = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewWrap.style.display = "block";
    nextBtn.style.display = "block";
    hideError();
  };
  reader.readAsDataURL(file);
}

// ── Step navigation ───────────────────────────────────────────────────────────
nextBtn.addEventListener("click", () => {
  stepUpload.classList.remove("active");
  stepPrefs.classList.add("active");
});

backBtn.addEventListener("click", () => {
  stepPrefs.classList.remove("active");
  stepUpload.classList.add("active");
});

// ── Option card selection ─────────────────────────────────────────────────────
function setupOptionCards(containerId, stateKey) {
  const container = document.getElementById(containerId);
  container.querySelectorAll(".option-card").forEach((card) => {
    card.addEventListener("click", () => {
      container.querySelectorAll(".option-card").forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
      state[stateKey] = card.dataset.value;
    });
  });
}
setupOptionCards("style-cards", "style");
setupOptionCards("mood-cards", "mood");
setupOptionCards("budget-cards", "budget");

// ── Generate design ───────────────────────────────────────────────────────────
designBtn.addEventListener("click", async () => {
  if (!state.file) return;

  stepPrefs.classList.remove("active");
  loading.style.display = "block";
  results.style.display = "none";
  hideError();

  const formData = new FormData();
  formData.append("image", state.file);
  formData.append("style", state.style);
  formData.append("mood", state.mood);
  formData.append("budget", state.budget);

  try {
    const res = await fetch(`${API_BASE}/design-room`, { method: "POST", body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Something went wrong.");
    state.design = data;
    renderResults(data);
  } catch (err) {
    showError(err.message || "Could not reach the server. Is the backend running on port 8000?");
    stepPrefs.classList.add("active");
  } finally {
    loading.style.display = "none";
  }
});

// ── Generate AI room render (debounced) ───────────────────────────────────────
let renderDebounceTimer = null;

function scheduleRender() {
  clearTimeout(renderDebounceTimer);
  renderDebounceTimer = setTimeout(triggerRender, 400);
}

async function triggerRender() {
  const design = state.design;
  if (!design) return;

  const selectedNames = Object.values(state.selectedProducts)
    .filter(Boolean)
    .map((p) => p.name);

  const skeleton = document.getElementById("render-skeleton");
  const renderImg = document.getElementById("ai-render-img");
  const statusEl = document.getElementById("render-status");

  skeleton.style.display = "flex";
  renderImg.style.display = "none";
  statusEl.textContent = "generating…";

  try {
    const res = await fetch(`${API_BASE}/generate-render`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        style: state.style,
        wall_color_name: state.selectedWallColor?.name || "Warm White",
        room_type: design.room_type || "living room",
        selected_products: selectedNames,
      }),
    });

    const data = await res.json();
    if (res.ok && data.image_data) {
      renderImg.src = data.image_data;
      renderImg.style.display = "block";
      skeleton.style.display = "none";
      statusEl.textContent = "✓ updated";
      setTimeout(() => { statusEl.textContent = ""; }, 2000);
    } else {
      skeleton.style.display = "none";
      renderImg.src = "";
      renderImg.style.display = "none";
      statusEl.textContent = "unavailable";
    }
  } catch {
    skeleton.style.display = "none";
    statusEl.textContent = "unavailable";
  }
}

// ── Render results ────────────────────────────────────────────────────────────
function renderResults(data) {
  document.getElementById("result-room-img").src = previewImg.src;
  document.getElementById("res-room-type").textContent = data.room_type || "Room";
  document.getElementById("res-design-summary").textContent = data.design_summary || "";

  const accent = data.accent_color || {};
  document.getElementById("res-accent-swatch").style.background = accent.hex || "#ccc";
  document.getElementById("res-accent-name").textContent = accent.name ? `Accent: ${accent.name}` : "";

  // Wall colors
  state.selectedWallColor = data.wall_color_options?.[0] || data.wall_color;
  renderWallColors(data.wall_color_options || [], data.wall_color);

  // Wall decor
  state.selectedDecorCost = data.wall_decor_options?.[0]?.landed_cost_usd || 0;
  state.selectedDecorId = data.wall_decor_options?.[0]?.id || null;
  renderWallDecor(data.wall_decor_options || []);

  // Products — default to first alternative per category
  state.selectedProducts = {};
  const byCategory = data.products_by_category || {};
  Object.entries(byCategory).forEach(([cat, products]) => {
    if (products.length) state.selectedProducts[cat] = products[0];
  });
  renderProducts(byCategory);

  updateTotal();

  results.style.display = "block";
  results.scrollIntoView({ behavior: "smooth", block: "start" });

  // Trigger initial AI render
  triggerRender();
}

// ── Wall color picker ─────────────────────────────────────────────────────────
function renderWallColors(options, aiSuggested) {
  const grid = document.getElementById("wall-color-grid");
  grid.innerHTML = "";

  const allColors = [...options];
  if (aiSuggested && !allColors.find((c) => c.hex === aiSuggested.hex)) {
    allColors.unshift({ ...aiSuggested, description: "AI recommended" });
  }

  allColors.forEach((color, i) => {
    const el = document.createElement("div");
    el.className = "wall-color-swatch" + (i === 0 ? " selected" : "");
    el.innerHTML = `
      <div class="swatch-circle" style="background:${color.hex}"></div>
      <div class="swatch-info">
        <div class="swatch-name">${color.name}</div>
        <div class="swatch-desc">${color.description || ""}</div>
      </div>`;
    el.addEventListener("click", () => {
      grid.querySelectorAll(".wall-color-swatch").forEach((s) => s.classList.remove("selected"));
      el.classList.add("selected");
      state.selectedWallColor = color;
      scheduleRender();
    });
    grid.appendChild(el);
  });
}

// ── Wall decor picker ─────────────────────────────────────────────────────────
function renderWallDecor(options) {
  const grid = document.getElementById("decor-grid");
  grid.innerHTML = "";

  options.forEach((item, i) => {
    const el = document.createElement("div");
    el.className = "decor-card" + (i === 0 ? " selected" : "");
    el.innerHTML = `
      <div class="decor-name">${item.name}</div>
      <div class="decor-origin">${flagEmoji(item.origin_country)} ${item.origin_country}</div>
      <div class="decor-cost">Landed ${formatUSD(item.landed_cost_usd)}</div>`;
    el.addEventListener("click", () => {
      grid.querySelectorAll(".decor-card").forEach((c) => c.classList.remove("selected"));
      el.classList.add("selected");
      state.selectedDecorId = item.id;
      state.selectedDecorCost = item.landed_cost_usd;
      updateTotal();
    });
    grid.appendChild(el);
  });
}

// ── Product cards ─────────────────────────────────────────────────────────────
function renderProducts(byCategory) {
  const grid = document.getElementById("product-grid");
  grid.innerHTML = "";

  Object.entries(byCategory).forEach(([category, alternatives]) => {
    if (!alternatives.length) return;

    const block = document.createElement("div");
    block.className = "product-category-block";
    block.innerHTML = `<div class="category-label">${category}</div>`;

    const row = document.createElement("div");
    row.className = "product-alternatives";

    alternatives.forEach((product, i) => {
      const isSelected = i === 0;
      const card = buildProductCard(product, isSelected, category, row);
      row.appendChild(card);
    });

    block.appendChild(row);
    grid.appendChild(block);
  });
}

function buildProductCard(product, isSelected, category, row) {
  const card = document.createElement("div");
  card.className = "product-card" + (isSelected ? " selected" : "");

  card.innerHTML = `
    <div class="product-header">
      <div class="product-name">${product.name}</div>
      ${isSelected ? '<span class="selected-badge">✓ Selected</span>' : '<span class="alt-badge">Alternative</span>'}
    </div>
    <div class="product-row"><span>Origin</span><span>${flagEmoji(product.origin_country)} ${product.origin_country}</span></div>
    <div class="product-row"><span>HS Code</span><span>${product.hs_code}</span></div>
    <div class="product-row"><span>Unit Cost</span><span>${formatUSD(product.unit_cost_usd)}</span></div>
    <div class="product-row"><span>Duty (${product.duty_rate_pct}%)</span><span>+${formatUSD(product.duty_amount_usd)}</span></div>
    <div class="product-row"><span>Freight</span><span>+${formatUSD(product.freight_usd)}</span></div>
    <div class="landed-row"><span>Landed Cost</span><span>${formatUSD(product.landed_cost_usd)}</span></div>`;

  card.addEventListener("click", () => {
    row.querySelectorAll(".product-card").forEach((c) => {
      c.classList.remove("selected");
      const b = c.querySelector(".selected-badge, .alt-badge");
      if (b) { b.className = "alt-badge"; b.textContent = "Alternative"; }
    });
    card.classList.add("selected");
    const badge = card.querySelector(".alt-badge, .selected-badge");
    if (badge) { badge.className = "selected-badge"; badge.textContent = "✓ Selected"; }
    state.selectedProducts[category] = product;
    updateTotal();
    scheduleRender();
  });

  return card;
}

// ── Total ─────────────────────────────────────────────────────────────────────
function updateTotal() {
  const productTotal = Object.values(state.selectedProducts)
    .reduce((sum, p) => sum + (p?.landed_cost_usd || 0), 0);
  const total = productTotal + state.selectedDecorCost;
  document.getElementById("res-total").textContent = formatUSD(total);
}

// ── Reset ─────────────────────────────────────────────────────────────────────
resetBtn.addEventListener("click", () => {
  state = { file: null, style: "modern", mood: "light", budget: "1000",
            design: null, selectedWallColor: null, selectedDecorId: null,
            selectedDecorCost: 0, selectedProducts: {} };
  fileInput.value = "";
  previewWrap.style.display = "none";
  nextBtn.style.display = "none";
  results.style.display = "none";
  hideError();
  stepUpload.classList.add("active");
  stepPrefs.classList.remove("active");

  // Reset all option card selections
  document.querySelectorAll("#style-cards .option-card").forEach((c, i) => {
    c.classList.toggle("selected", i === 0);
  });
  document.querySelectorAll("#mood-cards .option-card").forEach((c, i) => {
    c.classList.toggle("selected", i === 0);
  });
  document.querySelectorAll("#budget-cards .option-card").forEach((c, i) => {
    c.classList.toggle("selected", i === 1);
  });

  window.scrollTo({ top: 0, behavior: "smooth" });
});

// ── Helpers ───────────────────────────────────────────────────────────────────
function showError(msg) { errorBox.textContent = "⚠️ " + msg; errorBox.style.display = "block"; }
function hideError() { errorBox.style.display = "none"; }

function formatUSD(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(n || 0);
}

const FLAGS = {
  "China":"🇨🇳","Vietnam":"🇻🇳","India":"🇮🇳","Indonesia":"🇮🇩","Mexico":"🇲🇽",
  "Poland":"🇵🇱","Portugal":"🇵🇹","Italy":"🇮🇹","Malaysia":"🇲🇾",
  "United Kingdom":"🇬🇧","New Zealand":"🇳🇿","Turkey":"🇹🇷","Brazil":"🇧🇷",
};
function flagEmoji(c) { return FLAGS[c] || "🌍"; }
