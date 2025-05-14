// Dark mode toggle with localStorage and CSS variables
(function() {
  var darkModeClass = 'dark-mode';
  var buttonId = 'dark-mode-toggle-btn';
  var darkModeVars = {
    '--body-color': '#181a1b',
    '--background-color': '#181a1b',
    '--text-color': '#f4f4f4',
    '--heading-color': '#f8f8f8',
    '--subheading-color': '#cccccc',
    '--link-color': '#4ea1ff',
    '--code-background-color': '#23272e'
  };
  var lightModeVars = {
    '--body-color': '#f6f7fa',
    '--background-color': '#f6f7fa',
    '--text-color': '#23272e',
    '--heading-color': '#23272e',
    '--subheading-color': '#7a8288',
    '--link-color': '#0055bb',
    '--code-background-color': '#f3f4f6'
  };

  function setCSSVars(vars) {
    for (var key in vars) {
      document.documentElement.style.setProperty(key, vars[key]);
    }
  }

  function enableDarkMode() {
    document.body.classList.add(darkModeClass);
    setCSSVars(darkModeVars);
    localStorage.setItem('darkMode', 'enabled');
  }

  function disableDarkMode() {
    document.body.classList.remove(darkModeClass);
    setCSSVars(lightModeVars);
    localStorage.setItem('darkMode', 'disabled');
  }

  function toggleDarkMode() {
    if (document.body.classList.contains(darkModeClass)) {
      disableDarkMode();
    } else {
      enableDarkMode();
    }
  }

  // Add button if not present
  function addButton() {
    if (!document.getElementById(buttonId)) {
      var btn = document.createElement('button');
      btn.id = buttonId;
      btn.innerText = '🌙 Dark Mode';
      btn.style.position = 'fixed';
      btn.style.bottom = '24px';
      btn.style.right = '24px';
      btn.style.zIndex = 1000;
      btn.style.padding = '0.5em 1.2em';
      btn.style.background = '#23272e';
      btn.style.color = '#fff';
      btn.style.border = 'none';
      btn.style.borderRadius = '6px';
      btn.style.cursor = 'pointer';
      btn.style.boxShadow = '0 2px 8px rgba(0,0,0,0.12)';
      btn.onclick = toggleDarkMode;
      document.body.appendChild(btn);
    }
  }

  // On load, set mode
  window.addEventListener('DOMContentLoaded', function() {
    addButton();
    if (localStorage.getItem('darkMode') === 'enabled') {
      enableDarkMode();
    } else {
      disableDarkMode();
    }
  });
})();
