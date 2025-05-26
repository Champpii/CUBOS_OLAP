from src.routes.categoria.categoria_route import CategoriaRoutes as C_R
from src.routes.fecha.fecha_route import FechaRoutes as F_R
from src.routes.marca.marca_route import MarcaRoutes as M_R
from src.routes.modelo.modelo_route import ModeloRoutes as MO_R
from src.routes.producto.producto_route import ProductoRoutes as P_R
from src.routes.ventas.ventas_route import VentasRoutes as VNT_R

from src.controllers.categoria.categoria_controller import CategoriaController as C_C
from src.controllers.Fecha.fecha_controller import FechaController as F_C
from src.controllers.marca.marca_controller import MarcaController as M_C
from src.controllers.modelo.modelo_controller import ModeloController as MO_C
from src.controllers.producto.producto_controller import ProductoController as P_C
from src.controllers.ventas.ventas_controller import VentasController as VNT_C

class AppInitializer:
    def __init__(self, app, db, models):
        """
        Inicializa la aplicación Flask con los controladores y rutas correspondientes.
        """
        self.app = app
        self.controllers(db, models)
        self.routes()

    # Métodos para obtener controladores
    def getCategoriaControllers(self): return self.categoria_controllers
    def getFechaControllers(self): return self.fecha_controllers
    def getMarcaControllers(self): return self.marca_controllers
    def getModeloControllers(self): return self.modelo_controllers
    def getProductoControllers(self): return self.producto_controllers
    def getVentasControllers(self): return self.ventas_controllers

    # Método para inicializar rutas
    def routes(self):
        self.categoria_routes = C_R(self.app, self)
        self.fecha_routes = F_R(self.app, self)
        self.marca_routes = M_R(self.app, self)
        self.modelo_routes = MO_R(self.app, self)
        self.producto_routes = P_R(self.app, self)
        self.ventas_routes = VNT_R(self.app, self)

    # Método para inicializar controladores
    def controllers(self, db, models):
        self.categoria_controllers = C_C(db)
        self.fecha_controllers = F_C(db, models)
        self.marca_controllers = M_C(db, models)
        self.modelo_controllers = MO_C(db, models)
        self.producto_controllers = P_C(db, models)
        self.ventas_controllers = VNT_C(db, models)
