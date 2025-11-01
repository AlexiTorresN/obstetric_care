// Añadir efecto de scroll suave
document.addEventListener('DOMContentLoaded', function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    document.querySelectorAll('.animate-in').forEach((el) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        observer.observe(el);
    });

    // Efecto hover mejorado para las cards
    const roleCards = document.querySelectorAll('.role-card');
    
    roleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });

    // Animación al hacer clic en una card
    roleCards.forEach(card => {
        const btn = card.querySelector('.role-btn');
        if (btn) {
            btn.addEventListener('click', function(e) {
                // Añadir efecto de ripple
                const ripple = document.createElement('span');
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(255, 255, 255, 0.6)';
                ripple.style.width = '100px';
                ripple.style.height = '100px';
                ripple.style.animation = 'ripple 0.6s ease-out';
                ripple.style.left = e.clientX - this.getBoundingClientRect().left - 50 + 'px';
                ripple.style.top = e.clientY - this.getBoundingClientRect().top - 50 + 'px';
                
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        }
    });
});

// Animación ripple CSS (agregar a landing.css)
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);