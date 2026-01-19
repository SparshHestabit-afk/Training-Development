const productContainer = document.getElementById("products");
const searchInput = document.getElementById("search");
const sortSelect = document.getElementById("sort");
const productCategory = document.querySelectorAll(".product-category-button");

let allProductsList = [];
let currentProductCategory = "all";

//fetching the products from the dummyjson api
async function fetchProducts() {
    try {
        const response = await fetch("https://dummyjson.com/products?limit=0");
        const data = await response.json();
        allProductsList = data.products;
        filteredProducts = [...allProductsList];
        renderProducts(filteredProducts);

    } catch (error) {
        productContainer.innerHTML = "<h1>Failed to load Products</h1>"
        console.error(error);
    }
}

fetchProducts();

//product rating (from numbers to stars)
function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStars = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStars ? 1 : 0);

    let starHTML = "";

    for (let i = 0; i < fullStars; i++) {
        starHTML += "★";
    }

    if (halfStars) {
        starHTML += "½";
    }

    for (let i = 0; i < emptyStars; i++) {
        starHTML += "☆";
    }

    return starHTML;
};

//rendering the fetched produccts
function renderProducts(products) {
    productContainer.innerHTML = "";

    if (products.length === 0) {
        productContainer.innerHTML = `<p class="no-results">No products found</p>`;
        return;
    }

    products.forEach((products, index) => {
        const productCard = document.createElement("div");
        productCard.className = "product-card";

        let badgeHTML = ""
        if (index % 3 === 0) {
            badgeHTML = '<span class="badge sale">SALE</span>';
        } else if (index % 3 === 1) {
            badgeHTML = '<span class="badge out">Out of Stock</span>';
        } else {
            badgeHTML = '<span class="badge new">NEW</span>';
        }

        productCard.innerHTML = `
            ${badgeHTML}
            <img src="${products.thumbnail}" alt="${products.title}">
            <div class="product-card-content">
            <h3>${products.title}</h3>
            <div class="stars">
            ${generateStars(products.rating)}
            <span class="rating-value">(${products.rating})</span>
            </div>
            <div class="price">${products.price}</div>
            </div>
            `;

        productContainer.appendChild(productCard);
    });
}

//Category Handling
productCategory.forEach(btn => {
    btn.addEventListener('click', () => {
        productCategory.forEach(btns => btns.classList.remove("active"));
        btn.classList.add("active");

        currentProductCategory = btn.dataset.category;
        applyFilters();
    });
})

//Implementation of Filters
function applyFilters() {
    let filtered = [...allProductsList];
    
    //category filter
    if (currentProductCategory !== "all") {
        filtered = filtered.filter(prod =>
            prod.category &&
            prod.category.includes(currentProductCategory)
        );
    }
    
    // search filter
    const query = searchInput.value.trim().toLowerCase();
    
    if (query) {
        filtered = filtered.filter(prod =>
            (prod.title.toLowerCase().includes(query) )|| 
            (prod.description.toLowerCase().includes(query))
        );
    }

    //sort filter
    if (sortSelect.value === "high") {
        filtered.sort((a, b) => b.price - a.price);
    } else if (sortSelect.value === "low") {
        filtered.sort((a, b) => a.price - b.price);
    } else {
        filtered = filtered;
    }

    renderProducts(filtered);
}

//Event Listners for the product cards
searchInput.addEventListener('input', applyFilters);
sortSelect.addEventListener('change', applyFilters);

