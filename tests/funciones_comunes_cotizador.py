from . import (pytest, Callable, RegistroDeCosto, cotizador, Material, ManoDeObra)

def assertarArchivoInexistente(archivo:str):
    assert not archivo.exists()

def crearDireccionDeArchivoInexistente(tmpdir, nombre_archivo:str) -> str:
    archivo = tmpdir / nombre_archivo

    return archivo

def crearArchivoConRegistrosAnteriores(tmpdir, nombre_archivo:str, registros_anteriores:list[RegistroDeCosto]):
    contenido_archivo = pasarListaRegistrosATexto(registros_anteriores)

    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido_archivo)

    return archivo

def crearArchivoConContenido(tmpdir, nombre_archivo:str, contenido:str) -> str:
    archivo = crearDireccionDeArchivoInexistente(tmpdir, nombre_archivo)

    # Escribimos contenido
    archivo.write(contenido)

    return archivo

def assertarContenidoDeArchivoEsElEsperado(archivo:str, contenido_esperado:list[str]):

    archivo_modificado = open(archivo,"r")
    lineas_archivo:list[str] = archivo_modificado.readlines()
    archivo_modificado.close() #CERRE EL ARCHIVO

    assert lineas_archivo == contenido_esperado

def pasarListaRegistrosATexto(lista_registros:list[RegistroDeCosto]) -> str:
    contenido_archivo_esperado:str = ""
    
    if(lista_registros != []):
        primer_registro:RegistroDeCosto = lista_registros[0]

        if(primer_registro.esMaterial()):
            contenido_archivo_esperado += f"{primer_registro.nombre},{primer_registro.densidad_str()},{primer_registro.precio_str()}"
        if(primer_registro.esManoDeObra()):
            contenido_archivo_esperado += f"{primer_registro.nombre},{primer_registro.precio}"


        for registro in lista_registros[1:]:
            if(registro.esMaterial()):
                contenido_archivo_esperado +=(f"\n{registro.nombre},{registro.densidad},{registro.precio}")
            if(registro.esManoDeObra()):
                contenido_archivo_esperado += (f"\n{registro.nombre},{registro.precio}")
    
    return contenido_archivo_esperado

def pasarListaRegistrosALineasParaArchivo(lista_registros:list[RegistroDeCosto]) -> list[str]:
    lineas_archivo_esperadas:list[str] = []
    #breakpoint()
    if(lista_registros != []):
        ultimo_registro:RegistroDeCosto = lista_registros[-1]

        for registro in lista_registros[:-1]:
            if(registro.esMaterial()):
                lineas_archivo_esperadas.append(f"{registro.nombre},{registro.densidad},{registro.precio}\n")
            if(registro.esManoDeObra()):
                lineas_archivo_esperadas.append(f"{registro.nombre},{registro.precio}\n")

        if(ultimo_registro.esMaterial()):
            lineas_archivo_esperadas.append(f"{ultimo_registro.nombre},{ultimo_registro.densidad_str()},{ultimo_registro.precio_str()}")
        if(ultimo_registro.esManoDeObra()):
            lineas_archivo_esperadas.append(f"{ultimo_registro.nombre},{ultimo_registro.precio}")
    
    return lineas_archivo_esperadas