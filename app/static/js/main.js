window.addEventListener('DOMContentLoaded', () => {

    let url = new URL(document.URL);
    let navLinks = document.querySelectorAll('#navbarToggler .nav-link');
    let activeNavLink = navLinks[0];

    function getNavLink (txt) {
        for (let i = 0; i < navLinks.length; i++) {
            if (navLinks[i].text == txt) {
                return navLinks[i];
            };
        };
    };

    navMapping = {
        '/': 'CV',
        '/notes': 'Notes',
        '/blog': 'Notes',
        '/blog/tag/projects': 'Projects',
    };

    for (key in navMapping) {
        if (url.pathname.startsWith(key)) {
                activeNavLink = getNavLink(navMapping[key]);
            };
    };

    activeNavLink.classList.add('active');
});
