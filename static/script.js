const elements = document.querySelectorAll('.card, .contact-section');

window.addEventListener('scroll', () => {
    elements.forEach(el => {
        let position = el.getBoundingClientRect().top;
        let screenHeight = window.innerHeight;

        if (position < screenHeight - 100) {
            el.style.opacity = 1;
            el.style.transform = "translateY(0)";
        }
    });
});