(function () {
  "use strict";
  const { el, money, byId, getCart, changeQty, clearCart, count, total, apiBase, MAX_QTY } = window.Cafe;
  const $ = (id) => document.getElementById(id);
  const STATUSES = ["Accepted", "Preparing", "Ready", "Collected"];

  function showMessage(node, text, kind) {
    node.textContent = text;
    node.className = "message" + (kind ? " " + kind : "");
  }

  // ---------- Cart ----------
  function renderCart() {
    const list = $("cart-items");
    const cart = getCart();
    list.replaceChildren();

    for (const [id, qty] of Object.entries(cart)) {
      const item = byId.get(id);
      const minus = qtyButton("−", "Remove one " + item.name, () => update(id, -1));
      const plus = qtyButton("+", "Add one " + item.name, () => update(id, 1));
      plus.disabled = qty >= MAX_QTY;

      list.append(
        el("li", { className: "cart-row" },
          el("span", { className: "cart-emoji", ariaHidden: "true", textContent: item.emoji }),
          el("div", {},
            el("div", { className: "cart-name", textContent: item.name }),
            el("div", { className: "cart-unit", textContent: money(item.price) + " each" })
          ),
          el("div", { className: "qty" }, minus, el("span", { textContent: qty }), plus),
          el("span", { className: "line-total", textContent: money(item.price * qty) })
        )
      );
    }

    const empty = Object.keys(cart).length === 0;
    $("cart-empty").hidden = !empty;
    $("summary-count").textContent = count();
    $("summary-total").textContent = money(total());
    $("place-order").disabled = empty;
  }

  function qtyButton(label, ariaLabel, onClick) {
    const b = el("button", { className: "btn-qty", type: "button", textContent: label });
    b.setAttribute("aria-label", ariaLabel);
    b.addEventListener("click", onClick);
    return b;
  }

  function update(id, delta) {
    changeQty(id, delta);
    renderCart();
  }

  // ---------- Place order ----------
  async function placeOrder(event) {
    event.preventDefault();
    const msg = $("order-message");
    const pickupName = $("pickup-name").value.trim();
    const email = $("email").value.trim();

    if (!pickupName) return showMessage(msg, "Please enter a name for pickup.", "error");
    if (!email || !$("email").checkValidity()) return showMessage(msg, "Please enter a valid email.", "error");

    const order = {
      pickupName,
      email,
      items: Object.entries(getCart()).map(([id, qty]) => ({ id, qty }))
    };

    const button = $("place-order");
    button.disabled = true;
    showMessage(msg, "Placing your order…");

    try {
      const api = apiBase();
      let orderId;
      if (!api) {
        // Demo mode until the Function App is deployed (see config.js).
        await new Promise((r) => setTimeout(r, 500));
        orderId = "demo-" + crypto.randomUUID();
      } else {
        const res = await fetch(api + "/api/orders", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(order)
        });
        const body = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(body.message || "The order could not be placed. Please try again.");
        orderId = body.orderId;
      }

      clearCart();
      $("order-view").hidden = true;
      $("confirm-view").hidden = false;
      $("confirm-text").textContent = api
        ? "Thanks, " + pickupName + "! We'll email you as your order moves along. Keep this order ID:"
        : "Demo mode: the API isn't connected yet, so nothing was sent. Sample order ID:";
      $("confirm-id").textContent = orderId;
      $("order-id").value = orderId;
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      showMessage(msg, err.message, "error");
      button.disabled = count() === 0;
    }
  }

  // ---------- Track order ----------
  function showSteps(status) {
    const reached = STATUSES.indexOf(status);
    $("status-steps").hidden = reached < 0;
    document.querySelectorAll("#status-steps li").forEach((li, i) => {
      li.classList.toggle("done", i <= reached);
    });
  }

  async function trackOrder(event) {
    event.preventDefault();
    const msg = $("track-message");
    const orderId = $("order-id").value.trim();
    if (!orderId) return;

    const api = apiBase();
    if (!api) {
      showMessage(msg, "Demo mode: status lookup works once the API is connected. Sample view below.");
      return showSteps("Preparing");
    }

    showMessage(msg, "Checking…");
    showSteps(null);
    try {
      const res = await fetch(api + "/api/orders/" + encodeURIComponent(orderId));
      if (res.status === 404) return showMessage(msg, "No order found with that ID.", "error");
      if (!res.ok) throw new Error("Could not check the order right now.");
      const body = await res.json();
      showMessage(msg, "Status: " + body.status, "success");
      showSteps(body.status);
    } catch (err) {
      showMessage(msg, err.message, "error");
    }
  }

  $("order-form").addEventListener("submit", placeOrder);
  $("track-form").addEventListener("submit", trackOrder);
  renderCart();
})();
