// Collection Carousel functionality
class CollectionCarousel {
    constructor(carouselId) {
        this.carousel = document.getElementById(carouselId);
        if (!this.carousel) return;
        
        this.track = this.carousel.querySelector('.carousel-track');
        this.cards = this.track.querySelectorAll('.collection-card');
        const collectionName = carouselId.replace('carousel-', '');
        this.prevBtn = document.querySelector(`[data-carousel="${collectionName}"].prev`);
        this.nextBtn = document.querySelector(`[data-carousel="${collectionName}"].next`);
        
        this.currentIndex = 0;
        this.cardWidth = 0;
        this.gap = 32; // 2rem in pixels
        this.visibleCards = this.getVisibleCards();
        
        this.init();
    }
    
    getVisibleCards() {
        const containerWidth = this.carousel.offsetWidth;
        const cardWithGap = this.cards[0].offsetWidth + this.gap;
        return Math.floor(containerWidth / cardWithGap);
    }
    
    init() {
        this.updateDimensions();
        this.updateButtons();
        
        this.prevBtn.addEventListener('click', () => this.prev());
        this.nextBtn.addEventListener('click', () => this.next());
        
        window.addEventListener('resize', () => {
            this.updateDimensions();
            this.updatePosition();
        });
    }
    
    updateDimensions() {
        this.cardWidth = this.cards[0].offsetWidth;
        this.visibleCards = this.getVisibleCards();
    }
    
    updatePosition() {
        const offset = -(this.currentIndex * (this.cardWidth + this.gap));
        this.track.style.transform = `translateX(${offset}px)`;
        this.updateButtons();
    }
    
    updateButtons() {
        const maxIndex = Math.max(0, this.cards.length - this.visibleCards);
        
        if (this.currentIndex === 0) {
            this.prevBtn.style.opacity = '0.3';
            this.prevBtn.style.cursor = 'not-allowed';
        } else {
            this.prevBtn.style.opacity = '1';
            this.prevBtn.style.cursor = 'pointer';
        }
        
        if (this.currentIndex >= maxIndex) {
            this.nextBtn.style.opacity = '0.3';
            this.nextBtn.style.cursor = 'not-allowed';
        } else {
            this.nextBtn.style.opacity = '1';
            this.nextBtn.style.cursor = 'pointer';
        }
    }
    
    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updatePosition();
        }
    }
    
    next() {
        const maxIndex = Math.max(0, this.cards.length - this.visibleCards);
        if (this.currentIndex < maxIndex) {
            this.currentIndex++;
            this.updatePosition();
        }
    }
}

// Collection-scoped lightbox functionality
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const lightboxClose = document.getElementById('lightbox-close');
const lightboxPrev = document.getElementById('lightbox-prev');
const lightboxNext = document.getElementById('lightbox-next');

let currentCollectionImages = [];
let currentImageIndex = 0;

function initCollectionLightboxes() {
    // For each collection section
    const collectionSections = document.querySelectorAll('.collection-section');
    
    collectionSections.forEach(section => {
        const cards = section.querySelectorAll('.collection-card');
        const collectionImages = Array.from(cards).map(card => 
            card.querySelector('img').src
        );
        
        // Add click listeners to each card in this collection
        cards.forEach((card, index) => {
            card.addEventListener('click', () => {
                openCollectionLightbox(collectionImages, index);
            });
        });
    });
}

function openCollectionLightbox(images, index) {
    currentCollectionImages = images;
    currentImageIndex = index;
    lightboxImg.src = currentCollectionImages[currentImageIndex];
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

function showPrevImage() {
    currentImageIndex = (currentImageIndex - 1 + currentCollectionImages.length) % currentCollectionImages.length;
    lightboxImg.src = currentCollectionImages[currentImageIndex];
}

function showNextImage() {
    currentImageIndex = (currentImageIndex + 1) % currentCollectionImages.length;
    lightboxImg.src = currentCollectionImages[currentImageIndex];
}

// Event listeners for lightbox
lightboxClose.addEventListener('click', closeLightbox);
lightboxPrev.addEventListener('click', showPrevImage);
lightboxNext.addEventListener('click', showNextImage);

// Close on background click
lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
        closeLightbox();
    }
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('active')) return;
    
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') showPrevImage();
    if (e.key === 'ArrowRight') showNextImage();
});

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    // Find all collection carousels and initialize them
    const collectionCarousels = document.querySelectorAll('.collection-carousel');
    collectionCarousels.forEach(carousel => {
        new CollectionCarousel(carousel.id);
    });
    
    // Initialize lightboxes
    initCollectionLightboxes();
});
