(function () {
  "use strict";
  const { el, icon, refreshIcons, money, changeQty, getCart, count, total, toast, MAX_QTY } = window.Cafe;
  const categories = window.CAFE_CATEGORIES;

  // Start on the category from the URL (menu.html?category=cold), else the first one.
  const requested = new URLSearchParams(location.search).get("category");
  let active = categories.some((c) => c.id === requested) ? requested : categories[0].id;

  function renderTabs() {
    const tabs = document.getElementById("tabs");
    tabs.replaceChildren();
    for (const cat of categories) {
      const tab = el("button", { className: "tab tone-" + cat.id, type: "button" }, icon(cat.icon), cat.name);
      tab.setAttribute("role", "tab");
      tab.setAttribute("aria-selected", String(cat.id === active));
      tab.addEventListener("click", () => {
        active = cat.id;
        history.replaceState(null, "", "?category=" + cat.id);
        render();
      });
      tabs.append(tab);
    }
  }

  function renderMenu() {
    const grid = document.getElementById("menu-grid");
    const cart = getCart();
    grid.replaceChildren();

    window.CAFE_MENU.filter((item) => item.category === active).forEach((item, i) => {
      const inCart = cart[item.id] || 0;
      const add = el("button", { className: "btn-add", type: "button" }, icon("plus"), "Add");
      add.setAttribute("aria-label", "Add " + item.name);
      add.disabled = inCart >= MAX_QTY;
      add.addEventListener("click", () => {
        changeQty(item.id, 1);
        toast(item.name + " added");
        render();
      });

      const card = el("li", { className: "menu-card tone-" + item.category },
        item.popular ? el("span", { className: "tag-popular" }, icon("star"), "Popular") : "",
        el("span", { className: "icon-bubble" }, icon(item.icon)),
        el("h3", { textContent: item.name }),
        el("p", { textContent: item.description }),
        el("div", { className: "card-row" },
          el("div", {},
            el("span", { className: "price", textContent: money(item.price) }),
            inCart ? el("span", { className: "in-cart", textContent: inCart + " in your order" }) : ""
          ),
          add
        )
      );
      card.style.animationDelay = i * 40 + "ms";
      grid.append(card);
    });
  }

  function renderCta() {
    const n = count();
    document.getElementById("sticky-cta").hidden = n === 0;
    document.getElementById("cta-text").textContent =
      "Review order · " + n + (n === 1 ? " item" : " items") + " · " + money(total());
  }

  function render() {
    renderTabs();
    renderMenu();
    renderCta();
    refreshIcons();
  }

  render();
})();
