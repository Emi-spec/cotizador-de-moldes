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

def extraerSoloRegistros(lineas_archivo:list[str]):

    linea_registros:list[str] = []

    for linea in lineas_archivo[:-1]: 
        linea_registros.append(linea[:-1])

    linea_registros.append(lineas_archivo[-1])

    return linea_registros

def verificarSaltosDeLineaCorrectos(lineas_archivo:list[str]):
    for linea in lineas_archivo[:-1]:
        assert linea[-1:] == "\n"

    assert lineas_archivo[-1][-1:] != "\n"

def assertarContenidoDeArchivoEsElEsperado(archivo:str, contenido_esperado:list[str]):

    archivo_modificado = open(archivo,"r")
    lineas_archivo:list[str] = archivo_modificado.readlines()
    archivo_modificado.close() #CERRE EL ARCHIVO

    # registros_esperados:list[str] = []

    # for linea in contenido_esperado[:-1]: 
    #     registros_esperados.append(linea[:-2])

    # registros_esperados.append(contenido_esperado[-1])
    #breakpoint()
    #chequeo de correctamente identado(?)
    verificarSaltosDeLineaCorrectos(lineas_archivo)

    registros_archivo = extraerSoloRegistros(lineas_archivo)
    registros_esperados = extraerSoloRegistros(contenido_esperado)

    for registro in registros_archivo:
        assert registro in registros_esperados

    assert len(registros_archivo) == len(registros_esperados)

    # assert lineas_archivo == contenido_esperado

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

#test data
mano_de_obra_aceptada:ManoDeObra = ManoDeObra("35")

lista_registros_aceptada:list[RegistroDeCosto] = [Material("Aluminio 7075", "2.8", "23.50"),
                                                  Material("Aluminio 5083", "3", "4.5"), 
                                                  Material("Acero Amutit", "8", "7.5"),
                                                  mano_de_obra_aceptada,
                                                  Material("Acero Especial K", 8, 11)]

lista_materiales_aceptada:list[Material] = [reg for reg in lista_registros_aceptada if reg.esMaterial()]


