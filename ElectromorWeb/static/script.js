// Script para mostrar alertas simples y mejorar la UX

document.addEventListener("DOMContentLoaded", () => {
    // Confirmación al enviar formularios
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", () => {
            alert("Datos enviados correctamente ✅");
        });
    });

    // Ejemplo: botón de logout
    const logoutBtn = document.querySelector("#logout");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            alert("Sesión cerrada");
        });
    }
});
