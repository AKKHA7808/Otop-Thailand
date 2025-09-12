// Global variables
let allProducts = [];
let filteredProducts = [];
let map;
let markers = [];

// DOM elements
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const provinceFilter = document.getElementById('provinceFilter');
const levelFilter = document.getElementById('levelFilter');
const productsGrid = document.getElementById('productsGrid');
const loading = document.getElementById('loading');
const noResults = document.getElementById('noResults');
const productModal = document.getElementById('productModal');
const closeModal = document.getElementById('closeModal');
const modalContent = document.getElementById('modalContent');

// Navigation
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    setupNavigation();
});

// Initialize the application
async function initializeApp() {
    try {
        loading.style.display = 'block';
        await loadProducts();
        setupFilters();
        displayProducts(allProducts);
        updateStats();
        loading.style.display = 'none';
    } catch (error) {
        console.error('Error initializing app:', error);
        loading.innerHTML = '<i class="fas fa-exclamation-triangle"></i><p>เกิดข้อผิดพลาดในการโหลดข้อมูล</p>';
    }
}

// Load products from JSON file
async function loadProducts() {
    try {
        const response = await fetch('data/otop_products.json');
        if (!response.ok) {
            throw new Error('Failed to load products');
        }
        allProducts = await response.json();
        filteredProducts = [...allProducts];
    } catch (error) {
        console.error('Error loading products:', error);
        throw error;
    }
}

// Setup filter options
function setupFilters() {
    // Category filter
    const categories = [...new Set(allProducts.map(product => product.category))];
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categoryFilter.appendChild(option);
    });

    // Province filter
    const provinces = [...new Set(allProducts.map(product => product.province))];
    provinces.sort();
    provinces.forEach(province => {
        const option = document.createElement('option');
        option.value = province;
        option.textContent = province;
        provinceFilter.appendChild(option);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Search input
    searchInput.addEventListener('input', debounce(handleSearch, 300));
    
    // Filter selects
    categoryFilter.addEventListener('change', handleSearch);
    provinceFilter.addEventListener('change', handleSearch);
    levelFilter.addEventListener('change', handleSearch);
    
    // Modal
    closeModal.addEventListener('click', closeProductModal);
    window.addEventListener('click', function(event) {
        if (event.target === productModal) {
            closeProductModal();
        }
    });
}

// Setup navigation
function setupNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Smooth scroll to section
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });
    
    // Update active nav on scroll
    window.addEventListener('scroll', debounce(updateActiveNav, 100));
}

// Update active navigation based on scroll position
function updateActiveNav() {
    const scrollPos = window.scrollY + 100;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

// Handle search and filtering
function handleSearch() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const selectedCategory = categoryFilter.value;
    const selectedProvince = provinceFilter.value;
    const selectedLevel = levelFilter.value;
    
    filteredProducts = allProducts.filter(product => {
        const matchesSearch = !searchTerm || 
            product.name.toLowerCase().includes(searchTerm) ||
            product.name_en.toLowerCase().includes(searchTerm) ||
            product.description.toLowerCase().includes(searchTerm) ||
            product.province.toLowerCase().includes(searchTerm) ||
            product.category.toLowerCase().includes(searchTerm) ||
            product.producer.toLowerCase().includes(searchTerm);
        
        const matchesCategory = !selectedCategory || product.category === selectedCategory;
        const matchesProvince = !selectedProvince || product.province === selectedProvince;
        const matchesLevel = !selectedLevel || product.otop_level.toString() === selectedLevel;
        
        return matchesSearch && matchesCategory && matchesProvince && matchesLevel;
    });
    
    displayProducts(filteredProducts);
    updateStats();
    updateMapMarkers();
}

// Display products in grid
function displayProducts(products) {
    if (products.length === 0) {
        productsGrid.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }
    
    productsGrid.style.display = 'grid';
    noResults.style.display = 'none';
    
    productsGrid.innerHTML = products.map(product => createProductCard(product)).join('');
    
    // Add click event listeners to product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('click', function() {
            const productId = parseInt(this.dataset.productId);
            showProductModal(productId);
        });
    });
}

// Create product card HTML
function createProductCard(product) {
    const stars = '★'.repeat(product.otop_level);
    const certificationBadges = product.certification.map(cert => 
        `<span class="certification">${cert}</span>`
    ).join('');
    
    return `
        <div class="product-card" data-product-id="${product.id}">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
                <div class="otop-level">${stars} ${product.otop_level}</div>
            </div>
            <div class="product-content">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-name-en">${product.name_en}</p>
                <div class="product-category">${product.category}</div>
                <div class="product-location">
                    <i class="fas fa-map-marker-alt"></i>
                    ${product.province}, ${product.district}
                </div>
                <div class="product-price">${product.price.toLocaleString()} ${product.currency}</div>
                <div class="product-description">${product.description}</div>
                <div class="certifications">${certificationBadges}</div>
            </div>
        </div>
    `;
}

// Show product modal
function showProductModal(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;
    
    const stars = '★'.repeat(product.otop_level);
    const certificationBadges = product.certification.map(cert => 
        `<span class="certification">${cert}</span>`
    ).join('');
    
    modalContent.innerHTML = `
        <div class="modal-product">
            <div class="modal-image">
                <img src="${product.image}" alt="${product.name}" onerror="this.src='https://via.placeholder.com/400x300?text=No+Image'">
                <div class="modal-otop-level">${stars} ${product.otop_level}</div>
            </div>
            <div class="modal-details">
                <h2>${product.name}</h2>
                <h3>${product.name_en}</h3>
                <div class="modal-category">${product.category}</div>
                <div class="modal-location">
                    <i class="fas fa-map-marker-alt"></i>
                    ${product.tambon}, ${product.district}, ${product.province}
                </div>
                <div class="modal-price">${product.price.toLocaleString()} ${product.currency}</div>
                <div class="modal-description">
                    <h4>รายละเอียด</h4>
                    <p>${product.description}</p>
                    <p class="description-en">${product.description_en}</p>
                </div>
                <div class="modal-producer">
                    <h4>ผู้ผลิต</h4>
                    <p>${product.producer}</p>
                    <p class="producer-en">${product.producer_en}</p>
                    <p><i class="fas fa-phone"></i> ${product.contact}</p>
                </div>
                <div class="modal-certifications">
                    <h4>การรับรอง</h4>
                    <div class="certifications">${certificationBadges}</div>
                </div>
                <div class="modal-coordinates">
                    <h4>พิกัด</h4>
                    <p><i class="fas fa-map-marker-alt"></i> ${product.lat}, ${product.long}</p>
                    <button onclick="showOnMap(${product.lat}, ${product.long})" class="btn-show-map">
                        <i class="fas fa-map"></i> แสดงในแผนที่
                    </button>
                </div>
            </div>
        </div>
    `;
    
    productModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

// Close product modal
function closeProductModal() {
    productModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Show product on map
function showOnMap(lat, lng) {
    closeProductModal();
    document.getElementById('map').scrollIntoView({ behavior: 'smooth' });
    
    setTimeout(() => {
        if (map) {
            map.setCenter({ lat: lat, lng: lng });
            map.setZoom(15);
        }
    }, 1000);
}

// Update statistics
function updateStats() {
    document.getElementById('totalProducts').textContent = allProducts.length;
    document.getElementById('totalProvinces').textContent = 
        new Set(allProducts.map(p => p.province)).size;
    document.getElementById('filteredProducts').textContent = filteredProducts.length;
}

// Initialize Google Map
function initMap() {
    // Center map on Thailand
    const thailandCenter = { lat: 15.8700, lng: 100.9925 };
    
    map = new google.maps.Map(document.getElementById('googleMap'), {
        zoom: 6,
        center: thailandCenter,
        styles: [
            {
                featureType: 'poi',
                elementType: 'labels',
                stylers: [{ visibility: 'off' }]
            }
        ]
    });
    
    addMapMarkers();
}

// Add markers to map
function addMapMarkers() {
    if (!map) return;
    
    // Clear existing markers
    markers.forEach(marker => marker.setMap(null));
    markers = [];
    
    filteredProducts.forEach(product => {
        if (product.lat && product.long) {
            const marker = new google.maps.Marker({
                position: { lat: product.lat, lng: product.long },
                map: map,
                title: product.name,
                icon: getMarkerIcon(product.category)
            });
            
            const infoWindow = new google.maps.InfoWindow({
                content: createInfoWindowContent(product)
            });
            
            marker.addListener('click', () => {
                // Close all other info windows
                markers.forEach(m => {
                    if (m.infoWindow) {
                        m.infoWindow.close();
                    }
                });
                infoWindow.open(map, marker);
            });
            
            marker.infoWindow = infoWindow;
            markers.push(marker);
        }
    });
}

// Update map markers when filtering
function updateMapMarkers() {
    // Update the simple map display with current filtered products
    const mapDiv = document.getElementById('googleMap');
    if (mapDiv && filteredProducts) {
        mapDiv.innerHTML = `
            <div style="
                width: 100%; 
                height: 400px; 
                background: linear-gradient(to bottom, #87CEEB, #90EE90);
                position: relative;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                color: #333;
                text-align: center;
                border: 2px solid #ddd;
            ">
                <div>
                    <h3>🗺️ OTOP Thailand Map</h3>
                    <p>Interactive map showing ${filteredProducts.length} OTOP products</p>
                    <div style="margin-top: 20px; font-size: 14px; max-height: 200px; overflow-y: auto;">
                        ${filteredProducts.slice(0, 8).map(p => 
                            `<div style="margin: 5px 0; padding: 2px 5px; background: rgba(255,255,255,0.7); border-radius: 5px;">
                                📍 ${p.name} - ${p.province} (${p.category})
                            </div>`
                        ).join('')}
                        ${filteredProducts.length > 8 ? `<div style="margin-top: 10px; font-style: italic;">... และอีก ${filteredProducts.length - 8} รายการ</div>` : ''}
                    </div>
                </div>
            </div>
        `;
    }
}

// Get marker icon based on category
function getMarkerIcon(category) {
    const iconColors = {
        'อาหาร': '#ff5722',
        'เครื่องดื่ม': '#ff5722',
        'ของใช้ของตะวัน': '#9c27b0',
        'สิ่งทอ': '#2196f3',
        'สมุนไพร': '#4caf50',
        'ขนมหวาน': '#ff9800'
    };
    
    const color = iconColors[category] || '#666666';
    
    return {
        url: `data:image/svg+xml,${encodeURIComponent(`
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30">
                <circle cx="12" cy="12" r="10" fill="${color}" stroke="#fff" stroke-width="2"/>
                <circle cx="12" cy="12" r="4" fill="#fff"/>
            </svg>
        `)}`,
        scaledSize: new google.maps.Size(30, 30),
        anchor: new google.maps.Point(15, 15)
    };
}

// Create info window content
function createInfoWindowContent(product) {
    const stars = '★'.repeat(product.otop_level);
    return `
        <div class="info-window">
            <h3>${product.name}</h3>
            <p class="info-category">${product.category}</p>
            <p class="info-location">${product.province}</p>
            <p class="info-price">${product.price.toLocaleString()} ${product.currency}</p>
            <p class="info-level">${stars} ${product.otop_level}</p>
            <button onclick="showProductModal(${product.id})" class="info-btn">
                ดูรายละเอียด
            </button>
        </div>
    `;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add CSS for modal and info window
const additionalStyles = `
<style>
.modal-product {
    padding: 2rem;
}

.modal-image {
    position: relative;
    margin-bottom: 2rem;
}

.modal-image img {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 10px;
}

.modal-otop-level {
    position: absolute;
    top: 15px;
    right: 15px;
    background: #ffd700;
    color: #333;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-weight: 600;
}

.modal-details h2 {
    font-size: 1.8rem;
    color: #333;
    margin-bottom: 0.5rem;
}

.modal-details h3 {
    font-size: 1.2rem;
    color: #666;
    font-style: italic;
    margin-bottom: 1rem;
}

.modal-details h4 {
    color: #333;
    margin: 1.5rem 0 0.5rem 0;
    font-size: 1.1rem;
}

.modal-category {
    display: inline-block;
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}

.modal-location {
    color: #666;
    margin-bottom: 1rem;
}

.modal-location i {
    color: #ff5722;
    margin-right: 0.5rem;
}

.modal-price {
    font-size: 1.5rem;
    font-weight: 700;
    color: #4caf50;
    margin-bottom: 1rem;
}

.description-en, .producer-en {
    color: #666;
    font-style: italic;
    margin-top: 0.5rem;
}

.btn-show-map {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 500;
    margin-top: 1rem;
    transition: all 0.3s ease;
}

.btn-show-map:hover {
    background: #5a6fd8;
    transform: translateY(-2px);
}

.info-window {
    padding: 1rem;
    min-width: 200px;
}

.info-window h3 {
    margin: 0 0 0.5rem 0;
    color: #333;
}

.info-window p {
    margin: 0.3rem 0;
    color: #666;
}

.info-category {
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.2rem 0.5rem;
    border-radius: 10px;
    display: inline-block;
    font-size: 0.8rem;
}

.info-price {
    font-weight: 600;
    color: #4caf50 !important;
}

.info-level {
    color: #ffd700 !important;
    font-weight: 600;
}

.info-btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 15px;
    cursor: pointer;
    margin-top: 0.5rem;
    width: 100%;
}

.info-btn:hover {
    background: #5a6fd8;
}
</style>
`;

// Add the additional styles to the document head
document.head.insertAdjacentHTML('beforeend', additionalStyles);