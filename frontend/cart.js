// Shared by all pages: cart storage, header badge, toast, small helpers.
window.Cafe = (function () {
  "use strict";

  const KEY = "campus-cafe-cart";
  const MAX_QTY = 10;
  const byId = new Map(window.CAFE_MENU.map((item) => [item.id, item]));

  // Cart lives in localStorage so it survives moving between pages.
  // Storage can be blocked (private mode), so fall back to memory.
  let memory = {};
  function read() {
    try {
      const data = JSON.parse(localStorage.getItem(KEY) || "{}");
      // Drop anything not on the current menu.
      return Object.fromEntries(Object.entries(data).filter(([id, q]) => byId.has(id) && q > 0));
    } catch {
      return memory;
    }
  }
  function write(cart) {
    memory = cart;
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch { /* memory only */ }
    updateBadge();
  }

  function getCart() { return read(); }

  function changeQty(id, delta) {
    const cart = read();
    const next = Math.min(MAX_QTY, (cart[id] || 0) + delta);
    if (next <= 0) delete cart[id];
    else cart[id] = next;
    write(cart);
    return next;
  }

  function clearCart() { write({}); }

  function count() {
    return Object.values(read()).reduce((sum, q) => sum + q, 0);
  }

  function total() {
    return Object.entries(read()).reduce((sum, [id, q]) => sum + byId.get(id).price * q, 0);
  }

  function updateBadge() {
    const badge = document.getElementById("cart-count");
    if (!badge) return;
    const n = count();
    badge.textContent = n;
    badge.hidden = n === 0;
  }

  let toastTimer;
  function toast(text) {
    let el = document.getElementById("toast");
    if (!el) {
      el = document.createElement("div");
      el.id = "toast";
      el.className = "toast";
      el.setAttribute("role", "status");
      document.body.append(el);
    }
    el.textContent = text;
    el.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove("show"), 1800);
  }

  // Tiny element builder: el("p", { className: "muted" }, "text", child)
  function el(tag, props, ...children) {
    const node = document.createElement(tag);
    Object.assign(node, props || {});
    for (const child of children) node.append(child);
    return node;
  }

  const money = (n) => "$" + n.toFixed(2);
  const apiBase = () => (window.CAFE_CONFIG.apiBaseUrl || "").replace(/\/$/, "");

  document.addEventListener("DOMContentLoaded", updateBadge);

  return { MAX_QTY, byId, getCart, changeQty, clearCart, count, total, toast, el, money, apiBase };
})();
