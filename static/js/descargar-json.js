function DescargarJSON(productos_json) {
  // Verificar que productos_json no sea undefined
  if (!productos_json) {
    console.log("No se recibió el JSON.");
    return;
  }
  // Crear el objeto Blob con el JSON
  var productos_json = JSON.stringify(productos_json, null, 2); // Convierte el array JSON a cadena
  var blob = new Blob([productos_json], { type: "application/json" });

  // Crear un enlace de descarga
  var enlace = document.createElement("a");
  enlace.href = URL.createObjectURL(blob); // Crea una URL temporal para el archivo
  enlace.download = "productos.json"; // Nombre del archivo a descargar

  // Simular un clic en el enlace para iniciar la descarga
  enlace.click();

  // Libera la URL temporal
  URL.revokeObjectURL(enlace.href);
}
