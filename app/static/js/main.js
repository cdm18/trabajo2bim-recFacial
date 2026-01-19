function entrenarModelo() {
    const btn = document.getElementById('btn-entrenar');
    const status = document.getElementById('entrenamiento-status');

    // desactivar boton
    btn.disabled = true;
    btn.textContent = "Entrenando...";
    status.textContent = "Iniciando proceso en segundo plano...";
    status.style.color = "#2563eb";

    // iniciamos el entrenamiento
    fetch('/entrenar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                status.textContent = "El modelo se está entrenando. Por favor espere...";

                // empezamos a preguntar cada segundo si ya terminó
                const intervalo = setInterval(() => {
                    fetch('/status')
                        .then(res => res.json())
                        .then(estado => {
                            if (!estado.training) {
                                // termino el entrenamiento!
                                clearInterval(intervalo);
                                status.textContent = "¡Entrenamiento finalizado con éxito!";
                                status.style.color = "#10b981";
                                btn.disabled = false;
                                btn.textContent = "Re-entrenar Modelo";

                                // limpiar mensaje despues de unos segundos
                                setTimeout(() => {
                                    status.textContent = "";
                                }, 5000);
                            }
                        });
                }, 1000); // 1000ms = 1 segundo

            } else {
                status.textContent = "Error: " + data.message;
                status.style.color = "#ef4444";
                btn.disabled = false;
                btn.textContent = "Re-entrenar Modelo";
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            status.textContent = "Error de conexión.";
            status.style.color = "#ef4444";
            btn.disabled = false;
            btn.textContent = "Re-entrenar Modelo";
        });
}
