// Asegúrate de que este script esté después de la inclusión de jQuery y SweetAlert2
function mostrarAlertaCancelar() {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Todos los datos ya ingresados se perderán",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar',
        cancelButtonText: 'No, seguir'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = usuariosUrl;
        }
    }).catch((error) => {
        console.error("Error al mostrar la alerta:", error);
    });
}
