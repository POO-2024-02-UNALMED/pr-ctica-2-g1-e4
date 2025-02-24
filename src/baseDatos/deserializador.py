import pickle
from src.gestorAplicacion.administracion.deuda import Deuda
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.persona import Persona
from src.gestorAplicacion.bodega.camisa import Camisa
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.bodega.proveedor import Proveedor
from src.gestorAplicacion.bodega.repuesto import Repuesto
from src.gestorAplicacion.venta import Venta


def deserializar():
    archivo = open("src/baseDatos/persistencia.txt", "rb")
    (listaEmpleadosTotal, prendasInventadasTotal, listaSedes,
     listaBancos, cuentaPrincipal,
     listaPersonas,
     codigosRegalo, montosRegalo,
     listaProveedores,listaDeudas,listaVentas) = pickle.load(archivo)
    
    Sede.setListaEmpleadosTotal(listaEmpleadosTotal)
    Sede.setPrendasInventadasTotal(prendasInventadasTotal)
    Sede.setListaSedes(listaSedes)
    Banco.setListaBancos(listaBancos)
    Banco.setCuentaPrincipal(cuentaPrincipal)
    Persona.setListaPersonas(listaPersonas)
    Venta.setCodigosRegalo(codigosRegalo)
    Venta.setMontosRegalo(montosRegalo)
    Proveedor.setListaProveedores(listaProveedores)
    Deuda.setListaDeudas(listaDeudas)
    Sede.setHistoialTotalVentas(listaVentas)
    
    archivo.close()