import pickle
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.persona import Persona
from src.gestorAplicacion.bodega.camisa import Camisa
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.bodega.proveedor import Proveedor
from src.gestorAplicacion.bodega.repuesto import Repuesto
from src.gestorAplicacion.venta import Venta
def serializar():
    archivo = open("src/baseDatos/persistencia.txt", "wb")
    pickle.dump((Sede.getListaEmpleadosTotal(), Sede.getPrendasInventadasTotal(), Sede.getListaSedes(),
                 Banco.getListaBancos(), Banco.getCuentaPrincipal(),
                 Persona.getListaPersonas(),
                 Venta.getCodigosRegalo(), Venta.getMontosRegalo(),
                  Proveedor.getListaProveedores()), archivo)
    archivo.close()
