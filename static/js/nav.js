function initializeNavigation() {
  const navBar = document.querySelector('.nav-bar');
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.getElementById('site-menu');

  if (!navBar || !toggle || !menu) {
    return;
  }

  const setMenuOpen = (isOpen) => {
    menu.hidden = !isOpen;
    navBar.classList.toggle('menu-open', isOpen);
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
  };

  toggle.addEventListener('click', () => {
    setMenuOpen(!navBar.classList.contains('menu-open'));
  });

  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      setMenuOpen(false);
    }
  });

  document.addEventListener('click', (event) => {
    if (!navBar.contains(event.target)) {
      setMenuOpen(false);
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setMenuOpen(false);
      toggle.focus();
    }
  });
}

document.addEventListener('DOMContentLoaded', initializeNavigation);
