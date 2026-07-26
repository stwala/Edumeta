(function () {
  const body = document.body;
  const toggles = document.querySelectorAll("[data-sidebar-toggle]");

  function setOpen(open) {
    body.setAttribute("data-sidebar", open ? "open" : "closed");
  }

  toggles.forEach(function (el) {
    el.addEventListener("click", function () {
      const isOpen = body.getAttribute("data-sidebar") !== "closed";
      setOpen(!isOpen);
    });
  });

  if (window.matchMedia("(max-width: 900px)").matches) {
    setOpen(false);
  }
})();
