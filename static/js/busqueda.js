function busqueda() {
    const textoIngresado = document.getElementById("search-bar").value.toLowerCase().trim() // Texto ingresado por el usuario
    const productos = document.querySelectorAll("#contenedor-productos > div"); // Selecciona todos los productos

    productos.forEach(producto => { // Recorre producto por producto
        const titulo = producto.querySelector("h1").textContent.toLowerCase()
        if (titulo.includes(textoIngresado)) { // Si el texto ingresado esta incluido dentro del titulo
            producto.style.display = "flex" // Lo muestra
        } else {
            producto.style.display = "none" // Lo oculta
        }
    })
}