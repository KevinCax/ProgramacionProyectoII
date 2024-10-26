document.addEventListener('DOMContentLoaded', function() {
    window.toggleEstadoUsuario = function(dpi, estadoActual) {
        document.getElementById("dpi_usuario_toggle").value = dpi;
        var nuevoEstado = estadoActual === 'activo' ? 'inactivo' : 'activo';
        document.getElementById("nuevo_estado_usuario").value = nuevoEstado;
        
        var btnConfirmar = document.getElementById("btn_confirmar_toggle");
        btnConfirmar.textContent = estadoActual === 'activo' ? 'Desactivar' : 'Activar';
        btnConfirmar.classList.remove('btn-success', 'btn-danger');
        btnConfirmar.classList.add(estadoActual === 'activo' ? 'btn-danger' : 'btn-success');
        
        $('#ToggleUsuarioModal').modal('show');
    };

    document.getElementById("form_toggle_estado").addEventListener("submit", function(event) {
        console.log("Formulario enviado");
        console.log("DPI:", document.getElementById("dpi_usuario_toggle").value);
        console.log("Nuevo estado:", document.getElementById("nuevo_estado_usuario").value);
    });
});

// Función para manejar los mensajes de SweetAlert
function mostrarMensaje(tipo, titulo, texto) {
    Swal.fire({
        icon: tipo,
        title: titulo,
        text: texto,
    });
}