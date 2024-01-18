// theme-switch.js

// Function to toggle dark mode
function toggleDarkMode() {
    const isDarkMode = document.body.classList.toggle("dark-mode");
    localStorage.setItem('darkMode', isDarkMode);
}

// Event listener for the toggle button
document.getElementById("theme-toggle").addEventListener('click', toggleDarkMode);

// Load theme preference from local storage
window.onload = function() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add("dark-mode");
    }
};