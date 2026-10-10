'''
El elemento central: la necesidad que publica la empresa. 
Crea el script `src/simular_retos.py`. 
Con la libreria **Faker** genera 500 filas falsas de la tabla `retos`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.
Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.
'''

from datetime import timedelta
import random
import uuid
import pandas as pd
from faker import Faker

Faker.seed(42)
random.seed(42)

#id (texto (UUID)), 
# nombre (texto), 
#descripcion (texto), acotar
# fecha_inicio (fecha), 
#fecha_fin (fecha), 
# estado (texto), acotar 
#id_empresa (texto (UUID)), 
#id_categoria (texto (UUID)), acotar
#id_prioridad (texto (UUID)). acotar 

#3 Establecer una constante para el numero de simulaciones

FILAS = 500
FAKER = Faker("es_CO")
ESTADOS = ["activo", "inactivo", "pendiente"]


def generar_ids_referencia(cantidad):
    return [
        str(uuid.UUID(int=random.getrandbits(128), version=4))
        for _ in range(cantidad)
    ]


# Cada lista se crea una vez; los retos comparten referencias de estos grupos.
IDS_EMPRESA = generar_ids_referencia(5)
IDS_CATEGORIA = generar_ids_referencia(5)
IDS_PRIORIDAD = generar_ids_referencia(5)
FECHA_INICIO = FAKER.date_between(start_date="-1y", end_date="+3m")  # Fecha de inicio aleatoria

#4. funcion para generar datos falsos de la tabla retos
def generar_datos_retos(numero_filas=FILAS):
    usuarios = []
    for _ in range(numero_filas):
        usuarios.append(
            {
                "id": str(uuid.uuid4()),
                "nombre": FAKER.sentence(nb_words=6).rstrip("."),
                "descripcion": FAKER.sentence(nb_words=12),
                "fecha_inicio": FECHA_INICIO,
                "fecha_fin": FECHA_INICIO + timedelta(days=random.randint(15, 180)),
                "estado": random.choice(ESTADOS),
                "id_empresa": random.choice(IDS_EMPRESA),
                "id_categoria": random.choice(IDS_CATEGORIA),
                "id_prioridad": random.choice(IDS_PRIORIDAD),
            }
        )
    return usuarios

#5 Convertir la lista de diccionarios a un DataFrame de pandas
# La funcion principal debe devolver el DataFrame para reutilizarlo desde otros scripts.
def generar_retos(n=500):
    df = pd.DataFrame(generar_datos_retos(numero_filas=n))
    df = ensuciar(df)
    df = duplicar_filas(df)
    return df

#7. preparar la simulacion para ensuciar mis datos

#7.1 Funcion para obtener una muestra de los datos 

def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

#7.2 Funcion auxiliar para cambiar valores de un texto 
def escribir_mal(texto):
    variantes = [texto.title(),texto.lower() ,texto.upper(),texto.capitalize(), f" {texto} ", "Andres"]
    return random.choice(variantes)

#7.3 Funcion Auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI", "1"])
    else:
        return random.choice(["NO", "0"])

#7.4 Funcion Principal para ensuciar los datos  simulados 
def ensuciar(datos_df):
    datos_df = datos_df.copy()
    datos_df["fecha_inicio"] = pd.to_datetime(datos_df["fecha_inicio"])
    datos_df["fecha_fin"] = pd.to_datetime(datos_df["fecha_fin"])

    # fecha_fin: 8% nulo y 5% anterior a fecha_inicio
    filas_nulas_fin = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas_nulas_fin, "fecha_fin"] = None

    filas_disponibles = datos_df.drop(index=filas_nulas_fin)
    # El 5% del total se selecciona dentro del 92% que no quedo nulo.
    filas_fecha_fin_anterior = obtener_muestra(filas_disponibles, 0.05 / 0.92)
    datos_df.loc[filas_fecha_fin_anterior, "fecha_fin"] = (
        datos_df.loc[filas_fecha_fin_anterior, "fecha_inicio"]
        - pd.to_timedelta(
            [random.randint(1, 30) for _ in filas_fecha_fin_anterior],
            unit="D",
        )
    )

    # Nombre: el 10% tenga espacios y 8% tenga mayusculas
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "nombre"] = "" + datos_df.loc[filas_elegidas, "nombre"] + " "


    #descripcion: el 12% de las descripciones no deberia tener ningun valor (None)
    filas_elegidas = obtener_muestra(datos_df, 0.12)
    datos_df.loc[filas_elegidas, "descripcion"] = None

    #Mezclar el formato de fecha de inicio 
    #ISO=> YYYY-MM-DD HH:MM:SS
    #LATINO=> DD/MM/YYYY HH:MM:SS
    iso = datos_df["fecha_inicio"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = datos_df["fecha_inicio"].dt.strftime("%d/%m/%Y %H:%M:%S")
    datos_df["fecha_inicio"] = iso 
    filas_elegidas = obtener_muestra(datos_df, 0.25)
    datos_df.loc[filas_elegidas, "fecha_inicio"] = latino.loc[filas_elegidas]

 
 #estado: Aplicar errores de escritura (variantes)

    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "estado"] = datos_df.loc[filas_elegidas, "estado"].map(escribir_mal)

    return datos_df

#duplicar filas: duplicar el 5% de las filas para simular duplicados

def duplicar_filas(datos_df, porcentaje=0.05):
    filas_duplicadas = datos_df.sample(
        frac=porcentaje,
        random_state=random.randint(0, 9999),
    )
    return pd.concat([datos_df, filas_duplicadas], ignore_index=True)


#8. Si se ejecuta directamente el archivo, se muestra el resultado para inspeccion.
if __name__ == "__main__":
    df = generar_retos()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
