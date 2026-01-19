function entrenarModelo() {
    const btn = document.getElementById('btn-entrenar');
    const status = document.getElementById('entrenamiento-status');

    // Desactivar botón y mostrar estado de carga
    btn.disabled = true;
    btn.textContent = "Entrenando...";
    status.textContent = "Procesando imágenes, por favor espere...";
    status.style.color = "#2563eb";

    fetch('/entrenar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                status.textContent = "¡Entrenamiento completado exitosamente!";
                status.style.color = "#10b981";
            } else {
                status.textContent = "Error: " + data.message;
                status.style.color = "#ef4444";
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            status.textContent = "Error de conexión con el servidor.";
            status.style.color = "#ef4444";
        })
        .finally(() => {
            // Restaurar botón
            btn.disabled = false;
            btn.textContent = "Re-entrenar Modelo";

            // Limpiar mensaje después de 5 segundos
            setTimeout(() => {
                status.textContent = "";
            }, 5000);
        });
}
