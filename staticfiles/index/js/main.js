/*$( document ).ready(function() {
    // Handler for .ready() called.
    alert('Todo bien');
  });*/


/*function eliminarEquipo(id) {
  document.getElementById("id_equipo_eliminar").value = id;
}

function eliminarArea(id) {
  document.getElementById("id_area_eliminar").value = id;
}

function marcarBajado(id) {
  document.getElementById("id_trabajo_materiales").value = id;
}

function editarEquipo(id, area, codigo, descripcion) {
  document.getElementById("id_equipo_editar").value = id;
  document.getElementById("area_editar").value = area;
  document.getElementById("codigo_editar").value = codigo;
  document.getElementById("descripcion_editar").value = descripcion;
}*/


/*function historialPreventivo(id,solicitadoh,supervisado,responsable, subtotalpiezas, subtotalmo, fecha) {
  
  document.getElementById("hist_preventivo_editar").value = id;
  document.getElementById("hist_solicitadoh").value = solicitadoh;
  document.getElementById("hist_supervisadoh").value = supervisado;
  document.getElementById("hist_responsable").value = responsable;
  document.getElementById("hist_subtotalpiezas").value = subtotalpiezas;
  document.getElementById("hist_subtotalmo").value = subtotalmo;
  document.getElementById("hist_fecha_programada_editar").value = fecha;
}

function editarPreventivo(id, fecha, contacto, piezas, actividades, comentarios, total) {
  
  document.getElementById("id_preventivo_editar").value = id;
  document.getElementById("fecha_editar").value = fecha;
  document.getElementById("contacto_editar").value = contacto;
  document.getElementById("actividades_editar").value = actividades;
  document.getElementById("comentarios_editar").value = comentarios;
  document.getElementById("piezas_editar").value = piezas;
  document.getElementById("total_editar").value = total;
}*/

/*function editarCorrectivo(id, equipo, fecha, solicitado, estado, responsable, actividades, subtotalmo, supervisado, falla) {
  
  document.getElementById("id_correctivo_editar").value = id;
  document.getElementById("equipo_editar").value = equipo;
  document.getElementById("fecha_editar").value = fecha;
  document.getElementById("actividades_editar").value = actividades;
  document.getElementById("solicitadoc_editar").value = solicitado;
  document.getElementById("estado_editar").value = estado;
  document.getElementById("responsablec_editar").value = responsable;
  document.getElementById("subtotalmo_editar").value = subtotalmo;
  document.getElementById("supervisadoc_editar").value = supervisado;
  document.getElementById("falla_editar").value = falla;
}

function eliminarCorrectivo(id) {
  document.getElementById("id_correctivo_eliminar").value = id;
}*/

/*function historialCorrectivo(id,solicitadoh,supervisado,responsable, subtotalpiezas, subtotalmo, fecha) {
  
  document.getElementById("hist_correctivo_editar").value = id;
  document.getElementById("hist_solicitadoh").value = solicitadoh;
  document.getElementById("hist_supervisadoh").value = supervisado;
  document.getElementById("hist_responsable").value = responsable;
  document.getElementById("hist_subtotalpiezas").value = subtotalpiezas;
  document.getElementById("hist_subtotalmo").value = subtotalmo;
  document.getElementById("hist_fecha_programada_editar").value = fecha;
}

function eliminarPreventivo(id) {
  document.getElementById("id_preventivo_eliminar").value = id;
}*/

function editarProducto(id, cantidad, descripcion, categoria, precio_unitario, costo_unitario, imagen_url) {
  document.getElementById("id_producto_editar").value = id;
  document.getElementById("cantidad_editar").value = cantidad;
  document.getElementById("descripcion_editar").value = descripcion;
  document.getElementById("categoria_editar").value = categoria;
  document.getElementById("precio_editar").value = precio_unitario;
  document.getElementById("costo_editar").value = costo_unitario;

  if (imagen_url) {
      document.getElementById("imagen_editar").src = imagen_url;
  } else {
      document.getElementById("imagen_editar").src = '';
  }
}



function EstadoProducto(codigo, estadoActual) {
  document.getElementById("codigo_producto").value = codigo;
  var nuevoEstado = estadoActual === 'activo' ? 'inactivo' : 'activo';
  document.getElementById("nuevo_estado_producto").value = nuevoEstado;
  
  var btnConfirmar = document.getElementById("btn_confirmar_toggle");
  btnConfirmar.textContent = estadoActual === 'activo' ? 'Desactivar' : 'Activar';
  btnConfirmar.classList.remove('btn-success', 'btn-danger');
  btnConfirmar.classList.add(estadoActual === 'activo' ? 'btn-danger' : 'btn-success');
  
  $('#ToggleProductoModal').modal('show');
}

// Agregar este evento para depuración
document.getElementById("form_toggle_estado").addEventListener("submit", function(event) {
  console.log("Formulario enviado");
  console.log("CODIGO:", document.getElementById("codigo_producto").value);
  console.log("Nuevo estado:", document.getElementById("nuevo_estado_producto").value);
});


function seleccionarCliente(nit, nombre, correo) {
  
  document.getElementById('nit_Cui').value = nit;
  document.getElementById('nombre').value = nombre;
  document.getElementById('correoElectronico').value = correo;

  // Asegúrate de que el modal se cierre correctamente
  $('#ClientesModal').modal('hide');
  
  // Opcional: Puedes agregar un mensaje de confirmación si es necesario
  Swal.fire({
      icon: 'success',
      title: 'Cliente Seleccionado',
      text: 'Has seleccionado a ' + nombre,
  });
}

function editarPersonal(id, nombre, correoElectronico, direccion, notas, estado) {
  document.getElementById("id_personal_editar").value = id;
  document.getElementById("nombre_editar").value = nombre;
  document.getElementById("correo_editar").value = correoElectronico;
  document.getElementById("direccion_editar").value = direccion;
  document.getElementById("notas_editar").value = notas;

}

function EstadoClientes(nit_Cui, estadoActual) {
  document.getElementById("nit_Cui_cliente").value = nit_Cui;
  var nuevoEstado = estadoActual === 'activo' ? 'inactivo' : 'activo';
  document.getElementById("nuevo_estado_cliente").value = nuevoEstado;
  
  var btnConfirmar = document.getElementById("btn_confirmar_toggle");
  btnConfirmar.textContent = estadoActual === 'activo' ? 'Desactivar' : 'Activar';
  btnConfirmar.classList.remove('btn-success', 'btn-danger');
  btnConfirmar.classList.add(estadoActual === 'activo' ? 'btn-danger' : 'btn-success');
  
  $('#ToggleClienteModal').modal('show');
}

// Agregar este evento para depuración
document.getElementById("form_toggle_estado").addEventListener("submit", function(event) {
  console.log("Formulario enviado");
  console.log("DPI / CUI:", document.getElementById("nit_Cui_cliente").value);
  console.log("Nuevo estado:", document.getElementById("nuevo_estado_cliente").value);
});



function borrarContent(){
  document.getElementById("search").value = "";
}

function generarCodigo() {
  fetch('/ruta/a/tu/vista/generar_codigo/')
      .then(response => response.json())
      .then(data => {
          if (data.codigo) {
              document.getElementById('id_codigo').value = data.codigo;
          } else {
              alert('Error al generar el código.');
          }
      })
      .catch(error => {
          console.error('Error:', error);
          alert('Error al generar el código.');
      });
}








function editarUsuario(dpi, nombre, correoElectronico, rol, notas) {
  // Establecer los valores en el formulario
  document.getElementById("dpi_usuario_editar").value = dpi;
  document.getElementById("nombre_editar").value = nombre;
  document.getElementById("correo_editar").value = correoElectronico;
  document.getElementById("rol_editar").value = rol;
  document.getElementById("notas_editar").value = notas;

  // Actualizar el título del modal si es necesario
  document.querySelector("#EditarUsuarioModal .modal-title").textContent = "Editar Usuario: " + nombre;

  // Mostrar el modal
  $('#EditarUsuarioModal').modal('show');
}


function toggleEstadoUsuario(dpi, estadoActual) {
  document.getElementById("dpi_usuario_toggle").value = dpi;
  var nuevoEstado = estadoActual === 'activo' ? 'inactivo' : 'activo';
  document.getElementById("nuevo_estado_usuario").value = nuevoEstado;
  
  var btnConfirmar = document.getElementById("btn_confirmar_toggle");
  btnConfirmar.textContent = estadoActual === 'activo' ? 'Desactivar' : 'Activar';
  btnConfirmar.classList.remove('btn-success', 'btn-danger');
  btnConfirmar.classList.add(estadoActual === 'activo' ? 'btn-danger' : 'btn-success');
  
  $('#ToggleUsuarioModal').modal('show');
}

// Agregar este evento para depuración
document.getElementById("form_toggle_estado").addEventListener("submit", function(event) {
  console.log("Formulario enviado");
  console.log("DPI:", document.getElementById("dpi_usuario_toggle").value);
  console.log("Nuevo estado:", document.getElementById("nuevo_estado_usuario").value);
});

/*function eliminarUsuario(id) {
  document.getElementById("id_usuario_eliminar").value = id;
}*/

function activarEspera(){
  const btn = document.getElementById("btn");
  btn.innerHTML = 'Generando ... <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
  btn.disabled = true;
}

$(document).ready(function () {

  $('#myTable').DataTable({
    "language": {
      "url": "../static/index/js/idiom.json"},
    "lengthMenu": [[10, 25, 50], [10, 25, 50]],
    dom: 'Bfrtip',
    buttons: [
      { extend: 'csv' },
      { extend: 'print'},
    ]
  });
  $('#table2').DataTable({
    "language": {
      "url": "../static/index/js/idiom.json"},
    "lengthMenu": [[10, 25, 50], [10, 25, 50]],
    dom: 'Bfrtip',
    buttons: [
      { extend: 'csv' },
      { extend: 'print'},
    ]
  });
  $('#table3').DataTable({
    "language": {
      "url": "../static/index/js/idiom.json"},
    "lengthMenu": [[10, 25, 50], [10, 25, 50]],
    dom: 'Bfrtip',
    buttons: [
      { extend: 'csv' },
      { extend: 'print'},
    ]
  });
});

function toggleEstadoUsuario(dpi, estadoActual) {
  document.getElementById("dpi_usuario_toggle").value = dpi;
  
  var boton = document.getElementById("boton_toggle_" + dpi);
  var nuevoEstado = estadoActual === 'activo' ? 'inactivo' : 'activo';
  
  boton.textContent = estadoActual === 'activo' ? 'Desactivar' : 'Activar';
  boton.classList.toggle('btn-danger');
  boton.classList.toggle('btn-success');
  
  // Opcional: actualizar un campo oculto con el nuevo estado
  document.getElementById("nuevo_estado_usuario").value = nuevoEstado;
  
  // Enviar el formulario
  document.getElementById("form_toggle_estado").submit();
}
