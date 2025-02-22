import pickle
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.persona import Persona
from src.gestorAplicacion.bodega.camisa import Camisa
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.bodega.proveedor import Proveedor
from src.gestorAplicacion.bodega.repuesto import Repuesto
from src.gestorAplicacion.venta import Venta

def deserializar():
    archivoBodega = open("src/baseDatos/bodega.txt", "rb")
    Camisa.setTipoInsumo(pickle.load(archivoBodega))
    Camisa.setCantidadInsumo(pickle.load(archivoBodega))
    Pantalon.setTipoInsumo(pickle.load(archivoBodega))
    Pantalon.setCantidadInsumo(pickle.load(archivoBodega))
    Proveedor.setListaProveedores(pickle.load(archivoBodega))
    archivoBodega.close()

    archivoSede = open("src/baseDatos/sede.txt", "rb")
    Sede.setListaEmpleadosTotal(pickle.load(archivoSede))
    Sede.setPrendasInventadasTotal(pickle.load(archivoSede))
    Sede.setListaSedes(pickle.load(archivoSede))
    archivoSede.close()
    print("Deserializamos estas sedes:")
    for sede in Sede.getListaSedes():
        print(sede.getNombre())

    archivoAdministracion = open("src/baseDatos/administracion.txt", "rb")
    Banco.setListaBancos(pickle.load(archivoAdministracion))
    Banco.setCuentaPrincipal(pickle.load(archivoAdministracion))
    archivoAdministracion.close()

    archivoPersona = open("src/baseDatos/persona.txt", "rb")
    Persona.setListaPersonas(pickle.load(archivoPersona))
    archivoPersona.close()

    archivoVenta = open("src/baseDatos/venta.txt", "rb")
    Venta.setCodigosRegalo(pickle.load(archivoVenta))
    Venta.setMontosRegalo(pickle.load(archivoVenta))
    archivoVenta.close()
