class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    def agregar(self, producto):
        id_producto = str(producto.id)
        if id_producto not in self.carrito.keys():
            if producto.stock > 0:
                self.carrito[id_producto] = {
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    # Convertimos el objeto Decimal a float para que JSON pueda leerlo
                    "precio": float(producto.precio), 
                    "cantidad": 1,
                    "total": float(producto.precio),
                    "imagen_url": producto.imagen_url
                }
        else:
            if producto.stock > self.carrito[id_producto]["cantidad"]:
                self.carrito[id_producto]["cantidad"] += 1
                self.carrito[id_producto]["total"] = float(self.carrito[id_producto]["precio"]) * self.carrito[id_producto]["cantidad"]
        self.guardar()

    def restar(self, producto):
        id_producto = str(producto.id)
        if id_producto in self.carrito.keys():
            self.carrito[id_producto]["cantidad"] -= 1
            self.carrito[id_producto]["total"] = float(self.carrito[id_producto]["precio"]) * self.carrito[id_producto]["cantidad"]
            if self.carrito[id_producto]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar()

    def eliminar(self, producto):
        id_producto = str(producto.id)
        if id_producto in self.carrito:
            del self.carrito[id_producto]
            self.guardar()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def guardar(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True