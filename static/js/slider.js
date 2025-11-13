class MuseumSlider {
    constructor(container) {
        this.container = container;
        this.track = container.querySelector('.slider-track');
        this.slides = Array.from(container.querySelectorAll('.slide'));
        this.prevBtn = container.querySelector('.slider-nav.prev');
        this.nextBtn = container.querySelector('.slider-nav.next');
        this.pagination = container.querySelector('.slider-pagination');
        this.counter = container.querySelector('.slide-counter');
        
        this.settings = {
            delay: parseInt(container.dataset.delay) * 1000 || 5000,
            loop: container.dataset.loop === 'true', // === '' для перевода в булевое значение
            showNavs: container.dataset.navs === 'true',
            showPagination: container.dataset.pags === 'true',
            autoPlay: container.dataset.auto === 'true',
            stopOnHover: container.dataset.stopHover === 'true'
        };
        
        this.currentIndex = 0;
        this.autoPlayInterval = null;
        this.totalSlides = this.slides.length;
        
        this.init();
    }
    
    init() {
        this.setupNavigation();
        this.setupPagination();
        this.setupCounter();
        this.applySettings();
        
        if (this.settings.autoPlay) { 
            this.startAutoPlay();
        }
        
        this.setupEventListeners(); 
        
        this.showSlide(0);
    }
    
    setupNavigation() {
        if (!this.settings.showNavs) {
            this.prevBtn.classList.add('hidden');
            this.nextBtn.classList.add('hidden');
            return;
        }
        
        this.prevBtn.addEventListener('click', () => this.prevSlide());
        this.nextBtn.addEventListener('click', () => this.nextSlide());
    }
    
    setupPagination() {
        if (!this.settings.showPagination) {
            this.pagination.classList.add('hidden');
            return;
        }
        
        this.slides.forEach((_, index) => { // _ - сам элемент не используется
            const dot = document.createElement('button');
            dot.className = 'pagination-dot';
            dot.addEventListener('click', () => this.showSlide(index));
            this.pagination.appendChild(dot);
        });
        
        this.updatePagination(); // выделение активной точки
    }
    
    setupCounter() { 
        this.updateCounter();
    }
    
    applySettings() { // избыточен
        if (!this.settings.showNavs) {
            this.prevBtn.style.display = 'none';
            this.nextBtn.style.display = 'none';
        }
        
        if (!this.settings.showPagination) {
            this.pagination.style.display = 'none';
        }
    }
    
    setupEventListeners() {
        if (this.settings.autoPlay && this.settings.stopOnHover) {
            this.container.addEventListener('mouseenter', () => this.stopAutoPlay());
            this.container.addEventListener('mouseleave', () => this.startAutoPlay());
        }
    }
    
    showSlide(index) {
        this.slides.forEach(slide => slide.classList.remove('active'));
        
        this.slides[index].classList.add('active');
        this.currentIndex = index;
        
        this.updatePagination();
        this.updateCounter();
    }
    
    nextSlide() {
        let nextIndex = this.currentIndex + 1;
        
        if (nextIndex >= this.totalSlides) {
            if (this.settings.loop) {
                nextIndex = 0;
            } else {
                nextIndex = this.totalSlides - 1;
            }
        }
        
        this.showSlide(nextIndex);
    }
    
    prevSlide() {
        let prevIndex = this.currentIndex - 1;
        
        if (prevIndex < 0) {
            if (this.settings.loop) {
                prevIndex = this.totalSlides - 1;
            } else {
                prevIndex = 0;
            }
        }
        
        this.showSlide(prevIndex);
    }
    
    updatePagination() {
        const dots = this.pagination.querySelectorAll('.pagination-dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentIndex);
        });
    }
    
    updateCounter() {
        this.counter.textContent = `${this.currentIndex + 1} / ${this.totalSlides}`;
    }
    
    startAutoPlay() {
        if (this.autoPlayInterval) return;
        
        this.autoPlayInterval = setInterval(() => {
            this.nextSlide();
        }, this.settings.delay);
    }
    
    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const sliderContainer = document.querySelector('.slider-container');
    if (sliderContainer) {
        new MuseumSlider(sliderContainer);
    }
});
