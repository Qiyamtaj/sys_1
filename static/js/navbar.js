// Apply initial styling on page load
window.onload = function() {
  var menu = document.getElementById('menu');
  var content = document.getElementById('content');
  menu.style.left = '-300px'; // Set the initial left position of the menu to hide it
  content.style.marginLeft = '0'; // Set the initial content margin to 0
  menu.style.transitionDuration = '0s';
};

function openMenu() {
  var menu = document.getElementById('menu');
  var content = document.getElementById('content');
  menu.style.left = '0';
  menu.style.transitionDuration = '0.6s';
  content.classList.add('menu-open');
  content.style.marginLeft = '300px'; // Adjust the content's left margin to accommodate the menu width
  content.style.transitionDuration = '0.6s'; // Add transition duration
}

function closeMenu() {
  var menu = document.getElementById('menu');
  var content = document.getElementById('content');
  menu.style.left = '-300px';
  menu.style.transitionDuration = '0.6s';
  content.classList.remove('menu-open');
  content.style.marginLeft = '0'; // Reset the content's left margin when the menu is closed
  content.style.transitionDuration = '0.6s'; // Add transition duration
}

function toggleDropDown() {
  var submenu = document.getElementById('submenu');
  var arrow = document.getElementById('arrow');
  submenu.classList.toggle('hidden');
  arrow.classList.toggle('rotate-180');
}
