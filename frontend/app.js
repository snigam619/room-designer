const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://localhost:8000"
  : "https://room-designer-production.up.railway.app";

// ── State ──────────────────────────────────────────────────────────────────────
let state = {
  file: null,
  style: "modern",
  mood: "light",
  budget: "1000",
  design: null,
  selectedWallColor: null,
  selectedProducts: {},
};

// ── DOM refs ───────────────────────────────────────────────────────────────────
const dropZone       = document.getElementById("drop-zone");
const fileInput      = document.getElementById("file-input");
const previewWrap    = document.getElementById("preview-wrap");
const previewImg     = document.getElementById("preview-img");
const designBtn      = document.getElementById("design-btn");
const loading        = document.getElementById("loading");
const errorBox       = document.getElementById("error-box");
const results        = document.getElementById("results");
const emptyState     = document.getElementById("empty-state");
const resetBtn       = document.getElementById("reset-btn");
const changePhotoBtn = document.getElementById("change-photo-btn");

// ── File upload ────────────────────────────────────────────────────────────────
dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener("change", () => { if (fileInput.files[0]) handleFile(fileInput.files[0]); });
changePhotoBtn?.addEventListener("click", () => { fileInput.value = ""; fileInput.click(); });

function handleFile(file) {
  state.file = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewWrap.style.display = "block";
    dropZone.style.display = "none";
    designBtn.disabled = false;
    hideError();
  };
  reader.readAsDataURL(file);
}

// ── Pill selection ─────────────────────────────────────────────────────────────
function setupPills(containerId, stateKey) {
  document.getElementById(containerId).querySelectorAll(".pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      document.getElementById(containerId).querySelectorAll(".pill").forEach((p) => p.classList.remove("selected"));
      pill.classList.add("selected");
      state[stateKey] = pill.dataset.value;
    });
  });
}
setupPills("style-cards", "style");
setupPills("mood-cards", "mood");
setupPills("budget-cards", "budget");

// ── Loading animation ──────────────────────────────────────────────────────────
let loadingStepTimer = null;
function startLoadingSteps() {
  const steps = ["lstep-1", "lstep-2", "lstep-3"];
  let i = 0;
  document.querySelectorAll(".lstep").forEach((s) => s.classList.remove("active"));
  document.getElementById("lstep-1")?.classList.add("active");
  loadingStepTimer = setInterval(() => {
    i = Math.min(i + 1, steps.length - 1);
    document.querySelectorAll(".lstep").forEach((s) => s.classList.remove("active"));
    document.getElementById(steps[i])?.classList.add("active");
    if (i === steps.length - 1) clearInterval(loadingStepTimer);
  }, 2200);
}
function stopLoadingSteps() {
  clearInterval(loadingStepTimer);
  document.querySelectorAll(".lstep").forEach((s) => s.classList.remove("active"));
}

// ── Generate design ────────────────────────────────────────────────────────────
designBtn.addEventListener("click", async () => {
  if (!state.file) return;

  emptyState.style.display = "none";
  results.style.display = "none";
  loading.style.display = "flex";
  hideError();
  startLoadingSteps();

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
    emptyState.style.display = "flex";
  } finally {
    loading.style.display = "none";
    stopLoadingSteps();
  }
});

// ── AI room render ─────────────────────────────────────────────────────────────
let renderDebounceTimer = null;
function scheduleRender() {
  clearTimeout(renderDebounceTimer);
  renderDebounceTimer = setTimeout(triggerRender, 800);
}

async function triggerRender() {
  const design = state.design;
  if (!design) return;

  const skeleton = document.getElementById("render-skeleton");
  const renderImg = document.getElementById("ai-render-img");
  const statusEl = document.getElementById("render-status");

  skeleton.style.display = "flex";
  renderImg.style.display = "none";
  statusEl.textContent = "generating…";

  const slowTimer = setTimeout(() => {
    const hint = skeleton.querySelector(".slow-hint");
    if (!hint) {
      const div = document.createElement("div");
      div.className = "slow-hint";
      div.style.cssText = "font-size:0.7rem;color:#aaa;margin-top:6px;text-align:center;padding:0 16px";
      div.textContent = "Almost there… this can take up to 30s";
      skeleton.appendChild(div);
    }
  }, 12000);

  const selectedNames = Object.values(state.selectedProducts).filter(Boolean).map(p => p.name);

  try {
    const res = await fetch(`${API_BASE}/generate-render`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        style: state.style,
        wall_color_name: state.selectedWallColor?.name || design.wall_color?.name || "Warm White",
        wall_color_hex: state.selectedWallColor?.hex || design.wall_color?.hex || "",
        room_type: design.room_type || "living room",
        selected_products: selectedNames,
        accent_color_name: design.accent_color?.name || "",
        design_summary: design.design_summary || "",
      }),
    });

    const data = await res.json();
    clearTimeout(slowTimer);
    if (res.ok && data.image_data) {
      renderImg.src = data.image_data;
      renderImg.style.display = "block";
      skeleton.style.display = "none";
      statusEl.textContent = "✓";
      setTimeout(() => { statusEl.textContent = ""; }, 2000);
    } else {
      showRenderUnavailable(skeleton);
      statusEl.textContent = "";
    }
  } catch {
    clearTimeout(slowTimer);
    showRenderUnavailable(skeleton);
    statusEl.textContent = "";
  }
}

function showRenderUnavailable(skeleton) {
  skeleton.innerHTML = `
    <div style="text-align:center;padding:20px">
      <div style="font-size:1.6rem;margin-bottom:8px">🎨</div>
      <div style="font-size:0.82rem;font-weight:600;color:#555;margin-bottom:4px">Render unavailable</div>
      <div style="font-size:0.72rem;color:#aaa;line-height:1.6">HF credits may be depleted.<br>Try again in a moment.</div>
    </div>`;
  skeleton.style.animation = "none";
  skeleton.style.background = "#fafaf8";
}

// ── Base room images (generated once, stored as static assets) ─────────────────
const BASE_ROOM_IMAGES = {
  "living room":  "rooms/living_room.jpg",
  "bedroom":      "rooms/bedroom.jpg",
  "dining room":  "rooms/dining_room.jpg",
  "home office":  "rooms/living_room.jpg",
};
function baseRoomImage(roomType) {
  const key = (roomType || "").toLowerCase().trim();
  return BASE_ROOM_IMAGES[key] || BASE_ROOM_IMAGES["living room"];
}

// ── Render results ─────────────────────────────────────────────────────────────
function renderResults(data) {
  document.getElementById("result-room-img").src = baseRoomImage(data.room_type);
  document.getElementById("res-room-type").textContent = data.room_type || "Room";
  document.getElementById("res-design-summary").textContent = data.design_summary || "";

  const accent = data.accent_color || {};
  document.getElementById("res-accent-swatch").style.background = accent.hex || "#ccc";
  document.getElementById("res-accent-name").textContent = accent.name || "";

  state.selectedWallColor = data.wall_color_options?.[0] || data.wall_color;
  renderWallColors(data.wall_color_options || [], data.wall_color);

  state.selectedProducts = {};
  const byCategory = data.products_by_category || {};
  Object.entries(byCategory).forEach(([cat, products]) => {
    if (products.length) state.selectedProducts[cat] = products[0];
  });
  renderProducts(byCategory);

  updateTotal();
  buildCategoryFilter(byCategory);

  results.style.display = "block";
  triggerRender();
}

// ── Wall color picker ──────────────────────────────────────────────────────────
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
        <div class="swatch-hex">${color.hex}</div>
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

// ── Product grid ───────────────────────────────────────────────────────────────
function renderProducts(byCategory) {
  const grid = document.getElementById("product-grid");
  grid.innerHTML = "";

  Object.entries(byCategory).forEach(([category, alternatives]) => {
    if (!alternatives.length) return;

    const block = document.createElement("div");
    block.className = "product-category-block";
    block.dataset.cat = category;
    block.innerHTML = `<div class="category-label">${category}</div>`;

    const row = document.createElement("div");
    row.className = "product-alternatives";

    alternatives.forEach((product, i) => {
      row.appendChild(buildProductCard(product, i === 0, category, row));
    });

    block.appendChild(row);
    grid.appendChild(block);
  });
}

function buildProductCard(product, isSelected, category, row) {
  const card = document.createElement("div");
  card.className = "product-card" + (isSelected ? " selected" : "");

  const brandName = product.brand || product.origin_country || "";
  const brandUrl  = product.product_url || "";
  const brandHtml = brandUrl
    ? `<a class="product-brand-row" href="${brandUrl}" target="_blank" rel="noopener" title="Shop on ${brandName}" onclick="event.stopPropagation()">
         <span class="brand-dot"></span>${brandName}
         <svg class="brand-ext-icon" width="10" height="10" viewBox="0 0 12 12" fill="none">
           <path d="M7 1h4v4M11 1L5 7M2 3H1v8h8v-1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
         </svg>
       </a>`
    : `<div class="product-brand-row"><span class="brand-dot"></span>${brandName}</div>`;
  card.innerHTML = `
    ${isSelected ? '<span class="selected-badge">✓</span>' : ''}
    <div class="product-name">${product.name}</div>
    ${brandHtml}
    <div class="landed-row"><span>Price</span><span>${formatUSD(product.landed_cost_usd)}</span></div>`;

  card.addEventListener("click", () => {
    row.querySelectorAll(".product-card").forEach((c) => {
      c.classList.remove("selected");
      const b = c.querySelector(".selected-badge");
      if (b) b.remove();
    });
    card.classList.add("selected");
    if (!card.querySelector(".selected-badge")) {
      const badge = document.createElement("span");
      badge.className = "selected-badge";
      badge.textContent = "✓";
      card.prepend(badge);
    }
    state.selectedProducts[category] = product;
    updateTotal();
    scheduleRender();
  });

  return card;
}

// ── Category filter — built dynamically from AI-detected products only ─────────
function buildCategoryFilter(byCategory) {
  const bar = document.getElementById("category-filter-bar");
  bar.innerHTML = "";

  // "All" pill shows all AI-recommended categories together
  const allPill = document.createElement("button");
  allPill.className = "cat-pill active";
  allPill.dataset.cat = "all";
  allPill.textContent = "All";
  bar.appendChild(allPill);

  // One pill per category Claude detected in the image — no extras
  Object.keys(byCategory).forEach((cat) => {
    const pill = document.createElement("button");
    pill.className = "cat-pill";
    pill.dataset.cat = cat;
    pill.textContent = cat;
    bar.appendChild(pill);
  });

  // Wire up clicks — filter in-place by showing/hiding category blocks
  bar.querySelectorAll(".cat-pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      bar.querySelectorAll(".cat-pill").forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");

      const cat = pill.dataset.cat;
      const productGrid = document.getElementById("product-grid");

      // Always use the main product-grid (no browse-grid for AI categories)
      productGrid.querySelectorAll(".product-category-block").forEach((block) => {
        if (cat === "all" || block.dataset.cat === cat) {
          block.style.display = "block";
        } else {
          block.style.display = "none";
        }
      });
    });
  });
}

// ── Total ──────────────────────────────────────────────────────────────────────
function updateTotal() {
  const total = Object.values(state.selectedProducts)
    .reduce((sum, p) => sum + (p?.landed_cost_usd || 0), 0);
  document.getElementById("res-total").textContent = formatUSD(total);
}

// ── Reset ──────────────────────────────────────────────────────────────────────
resetBtn.addEventListener("click", () => {
  state = { file: null, style: "modern", mood: "light", budget: "1000",
            design: null, selectedWallColor: null, selectedProducts: {} };
  fileInput.value = "";
  previewWrap.style.display = "none";
  dropZone.style.display = "block";
  designBtn.disabled = true;
  results.style.display = "none";
  emptyState.style.display = "flex";
  hideError();

  document.querySelectorAll("#style-cards .pill").forEach((c, i) => c.classList.toggle("selected", i === 0));
  document.querySelectorAll("#mood-cards .pill").forEach((c, i) => c.classList.toggle("selected", i === 0));
  document.querySelectorAll("#budget-cards .pill").forEach((c, i) => c.classList.toggle("selected", i === 1));
  window.scrollTo({ top: 0, behavior: "smooth" });
});

// ── Helpers ────────────────────────────────────────────────────────────────────
function showError(msg) { errorBox.textContent = "⚠️ " + msg; errorBox.style.display = "block"; }
function hideError() { errorBox.style.display = "none"; }

function formatUSD(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n || 0);
}

const FLAGS = {
  "China":"🇨🇳","Vietnam":"🇻🇳","India":"🇮🇳","Indonesia":"🇮🇩","Mexico":"🇲🇽",
  "Poland":"🇵🇱","Portugal":"🇵🇹","Italy":"🇮🇹","Malaysia":"🇲🇾",
  "United Kingdom":"🇬🇧","New Zealand":"🇳🇿","Turkey":"🇹🇷","Brazil":"🇧🇷",
};
function flagEmoji(c) { return FLAGS[c] || "🌍"; }
