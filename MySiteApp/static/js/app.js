document.addEventListener("DOMContentLoaded", function () {
    const wrapper = document.querySelector('.wrapper');
    const registerLink = document.querySelector('.register-link');
    const loginLink = document.querySelector('.login-link');

    const registerForm = document.querySelector('.form-box.register');
    const loginForm = document.querySelector('.form-box.login');

    // Show Register Form
    registerLink.onclick = (e) => {
        e.preventDefault();
        wrapper.classList.add('active'); // Optional for background animations

    
        setTimeout(() => {
            loginForm.classList.add('hidden'); // Fully hide after animation
            registerForm.classList.remove('hidden');
        },2500); // Match animation duration
    };

    // Show Login Form
    loginLink.onclick = (e) => {
        e.preventDefault();
        wrapper.classList.remove('active'); // Optional for background animations


        setTimeout(() => {
            registerForm.classList.add('hidden'); // Fully hide after animation
            loginForm.classList.remove('hidden');
        }, 2500); // Match animation duration
    };
});
