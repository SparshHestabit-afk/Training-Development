/* NAVBAR DROPDOWN */
const menuBtn = document.getElementById("menu-btn");
const navMenu = document.getElementById("nav-menu");

menuBtn.addEventListener("click", () => {
  navMenu.classList.toggle("show");
});

/* ACCORDION */
const faqHeaders = document.querySelectorAll(".faq-header");

faqHeaders.forEach(header => {
  header.addEventListener("click", () => {
    const item = header.parentElement;
    const isOpen = item.classList.contains("active");

    document.querySelectorAll(".faq-item").forEach(i => {
      i.classList.remove("active");
      i.querySelector(".icon").textContent = ">";
    });

    if (!isOpen) {
      item.classList.add("active");
      header.querySelector(".icon").textContent = ">";
    }
  });
});
