'''
Clasifica tematicamente los retos. Crea el script `src/simular_categorias.py`. Con la libreria **Faker** genera 250 filas falsas de la tabla `categorias`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.

OJO: `area_responsable` NO esta en el modelo de Backend II: es una columna EXTRA solo para este ejercicio de analisis, para poder agrupar. Dejala anotada como tal en el script.

'''

import random
import uuid
import pandas as pd
from faker import Faker

# 1. Sembrar semillas para reproducibilidad
random.seed(42)
Faker.seed(42)

# 2. Establecer constantes y opciones acotadas
FILAS = 250
CATEGORIAS = [
    "Logística", 
    "Innovación", 
    "Soporte Técnico", 
    "Infraestructura", 
    "Desarrollo de Software", 
    "Seguridad de la Información", 
    "Calidad", 
    "Experiencia de Usuario", 
    "Analítica de Datos", 
    "Operaciones"
]
AREAS = ["Tecnología", "Operaciones", "Finanzas", "Recursos Humanos", "Mercadeo", "Servicio al Cliente"]

# Instancia local para Colombia
falsito = Faker("es_CO")

# 3. Función generadora base con ID y descripciones reales
def generar_datos(numero_filas=FILAS):
    categorias = []
    
    # Lista de descripciones profesionales
    descripciones_reales = [
        "Gestión eficiente de la cadena de suministro y distribución de productos.",
        "Implementación de nuevas tecnologías y metodologías ágiles en los procesos.",
        "Atención y resolución de incidencias técnicas para los usuarios finales.",
        "Mantenimiento y optimización de la infraestructura tecnológica central.",
        "Diseño, construcción y despliegue de soluciones de software escalables.",
        "Protección de datos corporativos y gestión de políticas de acceso y seguridad.",
        "Aseguramiento de estándares de calidad en los entregables del proyecto.",
        "Mejora continua en la interacción y satisfacción de los usuarios.",
        "Procesamiento y análisis avanzado de datos para la toma de decisiones.",
        "Coordinación y control de las operaciones diarias de la organización."
    ]

    for i in range(1, numero_filas + 1):
        categorias.append({
            "id": f"CAT-{i:03d}",  # ID secuencial estructurado y limpio
            "nombre": random.choice(CATEGORIAS),
            "descripcion": random.choice(descripciones_reales),  # Descripción real en español
            "area_responsable": random.choice(AREAS)  # Columna extra solo para análisis
        })
    return categorias


# 7.1 Función para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=42).index


# 7.2 Función auxiliar para cambiar variantes de escritura en un texto
def escribir_mal(texto):
    variantes = [
        texto,
        texto.lower(),
        texto.upper(),
        f"  {texto}  ",
        texto.replace("ó", "o").replace("í", "i").replace("á", "a").replace("é", "e").replace("ú", "u")
    ]
    return random.choice(variantes)


# 7.4 Función principal para ensuciar los datos simulados
def ensuciar(datos_df): 
    datos_df = datos_df.copy()
    
    # Nombre: aplicar variantes de escritura (espacios, mayúsculas, sin tildes)
    filas_elegidas = obtener_muestra(datos_df, 0.4)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].map(escribir_mal)
    
    # Descripcion: el 15% de los datos no debe tener ningún valor (nulos / None)
    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "descripcion"] = None
    
    # Area responsable: el 10% de los datos no debe tener ningún valor (nulos / None)
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "area_responsable"] = None
    
    # Duplicados exactos: 8% de las filas repetidas tal cual
    cantidad_duplicados = int(len(datos_df) * 0.08)
    filas_a_duplicar = datos_df.sample(n=cantidad_duplicados, random_state=42)
    datos_df = pd.concat([datos_df, filas_a_duplicar], ignore_index=True)
    
    return datos_df


# 7.5 Función contenedora para cumplir con el estándar de importación
def generar_categorias(n=FILAS):
    df_base = pd.DataFrame(generar_datos(n))
    df_sucio = ensuciar(df_base)
    return df_sucio


# 7.6 Probar la función y bloque principal
if __name__ == "__main__":
    tabla_ordenada_categorias = generar_categorias(FILAS)

    print("=" * 45)
    print("RESUMEN DE LA TABLA DE CATEGORIAS")
    print("=" * 45)

    # Mostrar el tamaño de la tabla
    filas, columnas = tabla_ordenada_categorias.shape
    print(f"La tabla tiene {filas:,} filas y {columnas} columnas.")

    # Mostrar filas
    print("\nPrimeras (n_filas) filas de la tabla:")
    print(tabla_ordenada_categorias.head(40))

    # Revisar si hay datos faltantes
    nulos_por_columna = tabla_ordenada_categorias.isna().sum()
    total_nulos = nulos_por_columna.sum()

    print("\nRevision de datos faltantes:")

    if total_nulos == 0:
        print("No hay valores nulos en la tabla.")
    else:
        print(f"Se encontraron {total_nulos} valores nulos:")

        # Mostrar las columnas que tienen valores nulos
        nulos_filtrados = nulos_por_columna[nulos_por_columna > 0]

        for columna, cantidad in nulos_filtrados.items():
            print(f"La columna '{columna}' tiene {cantidad} valores nulos.")

    print("=" * 45)
