"""
Define el nivel de atencion del reto. Crea el script `src/simular_prioridades.py`. Con la libreria **Faker** genera 200 filas falsas de la tabla `prioridades`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.

OJO: `dias_max_respuesta` NO esta en el modelo de Backend II: es una columna EXTRA solo para este ejercicio de analisis. Dejala anotada como tal en el script.
"""

import random
import uuid
from faker import Faker
import pandas as pd

#1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. Identificar los datos a simular con su tipo de dato
#id (texto (UUID))
#nombre (texto) *********
#nivel (entero)
#dias_max_respuesta (entero)

#3. ESTABLECER UNA CONSTANTE PARA EL NUMERO DE SIMULACIONES
FILAS=200
NIVELES=["Baja", "Media", "Alta", "Urgente", "Critica"]
FALSITO=Faker("es_CO")
NUMEROS_A_TEXTO = ["uno", "dos", "tres", "cuatro"]

#4. Funcion generadora
def generar_datos(numero_filas=200):
  list_prioridades=[]
  for _ in range(numero_filas):
    list_prioridades.append({
      "id": str(uuid.uuid4()),
      "nombre": random.choice(NIVELES),
      "nivel": random.choice(range(len(NIVELES))) + 1,
      "dias_max_respuesta": random.randint(1,25)
    })
  return list_prioridades

#5. Convirtiendo los datos generados en un dateframe con PANDAS
tabla_ordenada_prioridades=pd.DataFrame(generar_datos())

#6. PROBAR FUNCION
#print(tabla_ordenada_prioridades)


#7. PREPARAR LA SIMULACION PARA ENSUCIAR MIS DATOS

#7.1 FUNCION PARA OBTENER UNA MUESTRA DE LOS DATOS

def obtener_muestra(datos,porcentaje):
  return datos.sample(frac=porcentaje,random_state=random.randint(0,9999)).index
  #return datos.sample(fraccion=porcentaje,random_state=random.randint(0,9999)).index

#7.2 FUNCION AUXILIAR PARA CAMBIAR VALORES DE UN TEXTO
def escribir_mal(texto):
  variantes=[texto.lower(), texto.title(), texto.capitalize(), f" {texto} "]
  return random.choice(variantes)

#7.4 FUNCION PRINCIPAL PARA ENSUCIAR LOS DATOS SIMULADOS
def ensuciar(datos_df):
  datos_df=datos_df.copy()

  #Nombre: 15% con variantes: 'ALTA', ' alta ', 'Alta'.
  filas_elegidas=obtener_muestra(datos_df,0.15)
  datos_df.loc[filas_elegidas, "nombre"]=datos_df.loc[filas_elegidas, "nombre"].map(escribir_mal)

  #Nivel: a veces como TEXTO ('3'), a veces la palabra ('tres') y 7% en None.
  datos_df["nivel"]=datos_df["nivel"].astype(object)
  filas_elegidas=obtener_muestra(datos_df, 0.09)
  datos_df.loc[filas_elegidas, "nivel"]=datos_df.loc[filas_elegidas, "nivel"].astype(str)

  datos_df["nivel"]=datos_df["nivel"].astype(object)
  filas_elegidas=obtener_muestra(datos_df, 0.1)
  datos_df.loc[filas_elegidas, "nivel"]=random.choice(NUMEROS_A_TEXTO)

  datos_df["nivel"]=datos_df["nivel"].astype(object)
  filas_elegidas=obtener_muestra(datos_df, 0.07)
  datos_df.loc[filas_elegidas, "nivel"]=None

  #dias_max_respuesta: 5% en None y 3% con un valor absurdo (999)
  filas_elegidas=obtener_muestra(datos_df, 0.05)
  datos_df.loc[filas_elegidas, "dias_max_respuesta"]=None

  filas_elegidas=obtener_muestra(datos_df, 0.03)
  datos_df.loc[filas_elegidas, "dias_max_respuesta"]=999

  #8% de las filas repetidas tal cual (duplicados exactos)
  cantidad_duplicados=int(len(datos_df) * 0.08)
  filas_a_duplicar=datos_df.sample(n=cantidad_duplicados, random_state=42)
  datos_df=pd.concat([datos_df, filas_a_duplicar], ignore_index=True)

  return datos_df

def generar_prioridades(n=200):
  df_base=pd.DataFrame(generar_datos(n))
  df_sucio=ensuciar(df_base)
  return df_sucio

if __name__ == "__main__":
  tabla_ordenada_prioridades=generar_prioridades(FILAS)

  print("Resumen de la tabla PRIORIDADES")

  # Mostrar el tamaño de la tabla
  filas, columnas = tabla_ordenada_prioridades.shape
  print(f'La tabla tiene {filas} filas y {columnas} columnas.')

  # Mostrar filas
  primeras_filas=20
  print(f"\n Primeras {primeras_filas} filas")
  print(tabla_ordenada_prioridades.head(primeras_filas))

  # Revisar si hay datos faltantes
  print("\nConteo de valores nulos")
  print(tabla_ordenada_prioridades.isna().sum())