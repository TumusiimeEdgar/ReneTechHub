document.addEventListener('DOMContentLoaded', function () {
    const nav = document.getElementById('mainNav');
    if (nav) {
        const onScroll = () => {
            nav.classList.toggle('nav-scrolled', window.scrollY > 80);
        };
        onScroll();
        window.addEventListener('scroll', onScroll, { passive: true });
    }

    const navMenu = document.getElementById('navMenu');
    const mobileLinks = document.querySelectorAll('#navMenu .mobile-link');

    mobileLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const targetId = this.getAttribute('href');
            const targetEl = document.querySelector(targetId);
            if (!targetEl) return;

            const scrollToTarget = () => {
                const offset = 80;
                const top = targetEl.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: top, behavior: 'smooth' });
            };

            if (navMenu) {
                const offcanvasInstance = bootstrap.Offcanvas.getInstance(navMenu)
                    || bootstrap.Offcanvas.getOrCreateInstance(navMenu);
                navMenu.addEventListener('hidden.bs.offcanvas', function handler() {
                    navMenu.removeEventListener('hidden.bs.offcanvas', handler);
                    scrollToTarget();
                });
                offcanvasInstance.hide();
            } else {
                scrollToTarget();
            }
        });
    });

    const desktopLinks = document.querySelectorAll('#mainNav .nav-link[href^="#"]');
    const allNavLinks = [...desktopLinks, ...mobileLinks];

    allNavLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            allNavLinks.forEach(function (other) {
                other.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
});