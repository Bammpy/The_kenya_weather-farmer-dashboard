// Theme toggle (if you already have dark/light mode)
const toggle = document.getElementById('themeToggle');
const html = document.documentElement;

if (localStorage.getItem('theme') === 'light') {
    html.setAttribute('data-theme', 'light');
    toggle.innerHTML = '☀️';
} else {
    toggle.innerHTML = '🌙';
}

toggle.addEventListener('click', () => {
    if (html.getAttribute('data-theme') === 'light') {
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        toggle.innerHTML = '🌙';
    } else {
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        toggle.innerHTML = '☀️';
    }
});

// Blog filter functionality
document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const blogCards = document.querySelectorAll('.blog-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');

            const filterValue = this.getAttribute('data-filter');

            blogCards.forEach(card => {
                if (filterValue === 'all') {
                    card.style.display = 'block';
                } else {
                    if (card.getAttribute('data-category') === filterValue) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    });
});