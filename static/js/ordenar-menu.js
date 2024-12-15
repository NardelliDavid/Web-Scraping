function ordenar_menu() {
  document
    .getElementById("menu-ordenar")
    .classList.toggle("mostrar-menu-ordenar");
}

// Lista de productos guardada en un array
const productosOriginales = document.querySelectorAll(
  ".flex.justify-center.items-center.flex-col.gap-2.rounded-lg.w-96.h-96.bg-white.shadow"
); // Contenedor de cada producto
productosOriginalesArray = []; // Array donde van a estar guardados los productos
productosOriginales.forEach((i) => {
  // Recorre cada contenedor para buscar los productos
  const precioText = i.querySelector(".p_precio").textContent.trim(); // Obtiene el precio del producto
  const precioFloat = parseFloat(
    precioText.replace("$", "").replace(/\./g, "").replace(",", ".")
  ); // Convierte el precio a Float

  const producto = {
    img: i.querySelector("img").src,
    title: i.querySelector("h1").textContent,
    precio: precioFloat, // Precio con el que se ordenan los arrays
    precioFormateado: new Intl.NumberFormat("es-AR").format(precioFloat), // Precio con , para decimales
    href: i.querySelector("a") ? i.querySelector("a").href : null,
    pagina: i.querySelector("a").textContent,
  };
  productosOriginalesArray.push(producto); // Guarda los producto en un array
});
let ArrayProductos = Array.from(productosOriginalesArray); // Creamos una copia del array que sera ordenado

const contenedor = document.getElementById("contenedor-productos"); // Contenedor donde van los productos individualmentes

// Función para ordenar los productos
function ordenar_productos(criterio) {
  const h2_ordenar_por = document.querySelector("#h2-ordenar-por"); // H2 que dice Ordenar por
  if (criterio === "sin-ordenar") {
    h2_ordenar_por.innerHTML = "Ordenar por: Sin ordenar";
    mostrar_productos(productosOriginalesArray);
  } else if (criterio === "menor-precio") {
    h2_ordenar_por.innerHTML = "Ordenar por: Menor precio";
    ArrayProductos.sort((a, b) => a.precio - b.precio); // Ordena los productos antes de mostrarlos
    mostrar_productos(ArrayProductos);
  } else if (criterio === "mayor-precio") {
    h2_ordenar_por.innerHTML = "Ordenar por: Mayor precio";
    ArrayProductos.sort((a, b) => b.precio - a.precio); // Ordena los productos antes de mostrarlos
    mostrar_productos(ArrayProductos);
  }
  ordenar_menu(); // Cierra el menu despues de elegir el metodo de ordenamiento
  busqueda(); // Aplica la busqueda ingresada anteriormente
}

// Función para mostrar los productos en el contenedor
function mostrar_productos(array) {
  contenedor.innerHTML = ""; // Vacia el contenedor antes de agregar los productos
  array.forEach((producto) => {
    const itemDiv = document.createElement("div"); // Contenedor por cada producto
    itemDiv.classList.add(
      "flex",
      "justify-center",
      "items-center",
      "flex-col",
      "gap-2",
      "rounded-lg",
      "w-96",
      "h-96",
      "bg-white",
      "shadow"
    ); // Estilos del div

    // verifica si existe la pagina del producto
    if (producto.pagina) {
      // Verifica a que pagina pertenece el boton
      if (producto.pagina.includes("Xiaomi")) {
        colorBoton = "bg-orange-400 hover:bg-orange-600";
      } else if (producto.pagina.includes("Mercadolibre")) {
        colorBoton = "bg-yellow-400 hover:bg-yellow-600";
      } else if (producto.pagina.includes("Mercadositio")) {
        colorBoton = "bg-pink-600 hover:bg-pink-800";
      }
      // Variable del boton
      paginaButton = `<a href="${producto.href}" target="_blank" class="font-semibold py-2 px-4 rounded ${colorBoton} text-white">${producto.pagina}</a>`;
    }
    itemDiv.innerHTML = `
            <img src="${producto.img}" alt="${producto.title} IMG" class="w-48">
            <h1 class="text-lg text-center px-2">${producto.title}</h1>
            <span class="text-green-600 flex flex-row gap-1"><p class="precio">$${producto.precioFormateado}</p> en efectivo</span>
            ${paginaButton}
        `;

    contenedor.appendChild(itemDiv); // Agregar el producto al contenedor
  });
}
