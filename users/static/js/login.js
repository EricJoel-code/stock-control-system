document.getElementById('togglePassword').addEventListener('click', function () {
    const passwordInput = document.getElementById('password');
    const passwordIcon = document.getElementById('passwordIcon');
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';

    // Cambiar tipo del input
    passwordInput.setAttribute('type', type);

    // Cambiar ícono
    if (type === 'password') {
        passwordIcon.classList.remove('fa-eye-slash');
        passwordIcon.classList.add('fa-eye');
    } else {
        passwordIcon.classList.remove('fa-eye');
        passwordIcon.classList.add('fa-eye-slash');
    }
});
