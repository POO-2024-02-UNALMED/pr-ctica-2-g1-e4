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
    archivoBodega = open("src/baseDatos/bodega.txt", "wb")
    pickle.dump(Camisa.getTipoInsumo(), archivoBodega)
    pickle.dump(Camisa.getCantidadInsumo(), archivoBodega)
    pickle.dump(Pantalon.getTipoInsumo(), archivoBodega)
    pickle.dump(Pantalon.getCantidadInsumo(), archivoBodega)
    pickle.dump(Proveedor.getListaProveedores(), archivoBodega)
    archivoBodega.close()

    archivoSede = open("src/baseDatos/sede.txt", "wb")
    pickle.dump(Sede.getListaEmpleadosTotal(), archivoSede)
    pickle.dump(Sede.getPrendasInventadasTotal(), archivoSede)
    pickle.dump(Sede.getListaSedes(), archivoSede)
    archivoSede.close()

    archivoAdministracion = open("src/baseDatos/administracion.txt", "wb")
    pickle.dump(Banco.getListaBancos(), archivoAdministracion)
    pickle.dump(Banco.getCuentaPrincipal(), archivoAdministracion)
    archivoAdministracion.close()

    archivoPersona = open("src/baseDatos/persona.txt", "wb")
    pickle.dump(Persona.getListaPersonas(), archivoPersona)
    archivoPersona.close()

    archivoVenta = open("src/baseDatos/venta.txt", "wb")
    pickle.dump(Venta.getCodigosRegalo(), archivoVenta)
    pickle.dump(Venta.getMontosRegalo(), archivoVenta)
    archivoVenta.close()
