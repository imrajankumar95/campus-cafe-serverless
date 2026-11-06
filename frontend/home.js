(function () {
  "use strict";
  const { el, icon, refreshIcons } = window.Cafe;

  const grid = document.getElementById("category-grid");
  for (const cat of window.CAFE_CATEGORIES) {
    const count = window.CAFE_MENU.filter((item) => item.category === cat.id).length;
    grid.append(
      el("a", { className: "category-card tone-" + cat.id, href: "menu.html?category=" + cat.id },
        el("span", { className: "icon-bubble" }, icon(cat.icon)),
        el("h3", { textContent: cat.name }),
        el("p", { textContent: cat.blurb }),
        el("span", { className: "category-link" }, count + " items ", icon("arrow-right"))
      )
    );
  }
  refreshIcons();
})();
