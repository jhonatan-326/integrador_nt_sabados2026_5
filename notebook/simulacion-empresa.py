import random 
import uuid
import pandas as pd
from faker import Faker

# Sembrar semillas para los datos a simular (Garantiza reproducibilidad)
random.seed(42)
Faker.seed(42)

FILAS = 300
falso = Faker("es_CO")

# Función auxiliar para obtener una muestra de los índices de manera reproducible
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=42).index

# Función generadora de empresas
def generar_empresas(numero_filas = 300):
    df = []
    for _ in range(numero_filas):
        df.append({
            "id": str(uuid.uuid4()),
            "nombre": falso.company(),
            "nit": falso.numerify("#########-#"),
            "sector": random.choice(["agricola", "minero", "alimenticio", "industrial"]),
            "contacto": falso.name(),
            "correo": falso.email(),
            "telefono": falso.numerify("3#########"),
            "activo": random.choice([True, False])
        })
    return df

# Función para duplicar filas exactas (5%)
def agregar_duplicados_exactos(df, porcentaje=0.05):
    filas_a_duplicar = df.sample(frac=porcentaje, random_state=42)
    df_con_duplicados = pd.concat([df, filas_a_duplicar], ignore_index=True)
    return df_con_duplicados

# Función para duplicar NIT
def duplicar_nits_entre_empresas(df, porcentaje=0.03):
    df = df.copy()
    indices_destino = obtener_muestra(df, porcentaje)
    indices_origen = df.drop(index=indices_destino).sample(n=len(indices_destino), random_state=42).index
    df.loc[indices_destino, "nit"] = df.loc[indices_origen, "nit"].values
    return df

# Funciones auxiliares para ensuciar datos
def escribir_mal(texto):
    if not isinstance(texto, str):
        return texto
    variantes = [texto.lower(), texto.title(), texto.upper()]
    return random.choice(variantes)

def convertir_booleano(val):
    return random.choice(["si", "1", "no", "0"])

def numero_sucio(num):
    if not isinstance(num, str) or len(num) < 10:
        return num
    eleccion = [
        num, 
        num[:3] + " " + num[3:6] + " " + num[6:10], 
        "57+ " + num[:3] + "-" + num[3:6] + "-" + num[6:10]
    ]
    return random.choice(eleccion)

# Función principal para ensuciar los datos
def ensuciar(datos_df):
    datos_df = datos_df.copy()
    
    # Aplicar duplicidad de NITs (3%)
    datos_df = duplicar_nits_entre_empresas(datos_df, porcentaje=0.03)

    # Nombre: 10% con espacios adicionales y 15% en mayúsculas
    filas_elegidas = obtener_muestra(datos_df, 0.1)
    datos_df.loc[filas_elegidas, "nombre"] = " " + datos_df.loc[filas_elegidas, "nombre"] + " "

    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].str.upper()

    # NIT sucio
    filas_elegidas = obtener_muestra(datos_df, 0.5)
    nit = datos_df.loc[filas_elegidas, "nit"]
    datos_df.loc[filas_elegidas, "nit"] = (
        nit.str.slice(0, 3) + "."
        + nit.str.slice(3, 6) + "."
        + nit.str.slice(6, 9) + "-"
        + nit.str.slice(9, 10)
    )
    
    filas_elegidas = obtener_muestra(datos_df, 0.5)
    datos_df.loc[filas_elegidas, "nit"] = datos_df.loc[filas_elegidas, "nit"].str.replace("-", "", regex=False)

    # Sector sucio
    filas_elegidas = obtener_muestra(datos_df, 0.04)
    datos_df.loc[filas_elegidas, "sector"] = datos_df.loc[filas_elegidas, "sector"].apply(escribir_mal)

    # Contacto sucio
    filas_elegidas = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "contacto"] = None

    # Correo sucio
    filas_elegidas = obtener_muestra(datos_df, 0.06)
    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[filas_elegidas, "correo"].str.replace("@", "", regex=False)

    # Telefono sucio
    filas_elegidas = obtener_muestra(datos_df, 0.2)
    datos_df.loc[filas_elegidas, "telefono"] = datos_df.loc[filas_elegidas, "telefono"].apply(numero_sucio)

    # Activo sucio
    datos_df["activo"] = datos_df["activo"].astype(object)
    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "activo"] = datos_df.loc[filas_elegidas, "activo"].apply(convertir_booleano)

    return datos_df

# Bloque de ejecución principal
if __name__ == "__main__":
    df_base = pd.DataFrame(generar_empresas(FILAS))
    df_con_duplicados = agregar_duplicados_exactos(df_base, porcentaje=0.05)
    df_sucio = ensuciar(df_con_duplicados)
    
    print("--- DIMENSIONES DEL DATAFRAME (shape) ---")
    print(df_sucio.shape)
    
    print("\n--- PRIMERAS FILAS DE LA TABLA (head) ---")
    print(df_sucio.head())
    
    print("\n--- CONTEO DE DATOS NULOS POR COLUMNA (isna().sum) ---")
    print(df_sucio.isna().sum())