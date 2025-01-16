function busqueda() {
  const textoIngresado = document
    .getElementById("search-bar")
    .value.toLowerCase()
    .trim(); // Texto ingresado por el usuario
  const palabrasIngresadas = textoIngresado.split(/\s+/); // Divide el texto ingresado en palabras

  const productos = document.querySelectorAll("#contenedor-productos > div"); // Selecciona todos los productos

  productos.forEach((producto) => {
    const titulo = producto.querySelector("h1").textContent.toLowerCase(); // Título del producto
    const palabrasTitulo = titulo.split(/\s+/); // Divide el título en palabras

    // Comprueba si todas las palabras ingresadas están en el título
    const coincide = palabrasIngresadas.every((palabra) =>
      palabrasTitulo.some((palabraTitulo) => palabraTitulo.includes(palabra))
    );

    // Muestra u oculta el producto en función de la coincidencia
    producto.style.display = coincide ? "flex" : "none";
  });
}
