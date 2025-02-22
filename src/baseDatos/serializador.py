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
    archivoBodega = open("src/baseDatos/bodega", "wb")
    pickle.dump(Camisa.getTipoInsumo(), archivoBodega)
    pickle.dump(Camisa.getCantidadInsumo(), archivoBodega)
    pickle.dump(Pantalon.getTipoInsumo(), archivoBodega)
    pickle.dump(Pantalon.getCantidadInsumo(), archivoBodega)
    pickle.dump(Proveedor.getListaProveedores(), archivoBodega)
    pickle.dump(Repuesto.getListaRepuestos(), archivoBodega)
    archivoBodega.close()

    archivoSede = open("src/baseDatos/sede", "wb")
    pickle.dump(Sede.listaSedes, archivoSede)
    pickle.dump(Sede.getListaEmpleadosTotal(), archivoSede)
    pickle.dump(Sede.getListaClientesTotal(), archivoSede)
    pickle.dump(Sede.getListaEmpleadosTotal(), archivoSede)
    archivoSede.close()

    archivoAdministracion = open("src/baseDatos/administracion", "wb")
    pickle.dump(Banco.getListaBancos(), archivoAdministracion)
    pickle.dump(Banco.getCuentaPrincipal(), archivoAdministracion)
    archivoAdministracion.close()

    archivoPersona = open("src/baseDatos/persona", "wb")
    pickle.dump(Persona.getListaPersonas(), archivoPersona)
    archivoPersona.close()

    archivoVenta = open("src/baseDatos/venta", "wb")
    pickle.dump(Venta.getCodigosRegalo(), archivoVenta)
    pickle.dump(Venta.getListaVentas(), archivoVenta)
    archivoVenta.close()