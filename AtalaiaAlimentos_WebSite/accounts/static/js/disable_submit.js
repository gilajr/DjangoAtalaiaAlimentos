document.addEventListener('DOMContentLoaded', function () {
    var submitBtn = document.getElementById('submit-register-btn');
    
    submitBtn.addEventListener('click', function () {
        // Desativa o botão de envio quando clicado
        this.disabled = true;
        this.innerText = 'Enviando...';

        document.getElementById('register-form').addEventListener('submit', function () {
            submitBtn.disabled = false;
            submitBtn.innerText = 'Enviar';
        });
    });
});