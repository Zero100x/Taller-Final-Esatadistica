# =============================================================================
# ███████████████████████████████████████████████████████████████████████████████
# █                                                                           █
# █         TALLER FINAL DE ESTADÍSTICA - ANÁLISIS DE DATOS                   █
# █         Base de datos: Restaurantes USA v2                                █
# █                                                                           █
# ███████████████████████████████████████████████████████████████████████████████
# =============================================================================

# =============================================================================
# ████████████ BLOQUE 1: RECONOCIMIENTO DE DATOS ██████████████████████████████
# =============================================================================
# En este primer bloque importamos todas las librerías necesarias para el
# análisis y realizamos una exploración inicial de los datos para entender
# su estructura, tipos de variables y estadísticas básicas.
# =============================================================================

# --- 1.1 Importación de Librerías ---

# 'pandas' es la librería principal para manipulación y análisis de datos.
# Nos permite trabajar con DataFrames (tablas) de forma eficiente.
# La importamos con el alias 'pd' por convención universal en ciencia de datos.
import pandas as pd

# 'numpy' es la librería fundamental para cálculos numéricos en Python.
# Nos provee funciones matemáticas y el tipo especial 'NaN' (Not a Number)
# que usaremos para representar valores faltantes. Alias: 'np'.
import numpy as np

# 'matplotlib.pyplot' es la librería base de visualización en Python.
# La usamos para crear y personalizar gráficos (barras, torta, histograma, etc.).
# Alias: 'plt'.
import matplotlib.pyplot as plt

# 'seaborn' es una librería de visualización estadística construida sobre matplotlib.
# Ofrece gráficos más atractivos y funciones especializadas como boxplots.
# Alias: 'sns'.
import seaborn as sns

# 'math' es la librería estándar de Python para funciones matemáticas básicas
# como raíz cuadrada, potencias, logaritmos, etc.
import math

# Configuramos el estilo visual de seaborn para que todos los gráficos
# se vean con un fondo limpio y profesional. 'whitegrid' añade una cuadrícula
# gris claro que facilita la lectura de valores.
sns.set_style("whitegrid")

# Configuramos matplotlib para que los gráficos se muestren directamente
# dentro del notebook (inline). Esto es necesario en Jupyter Notebook.
# En Google Colab no es estrictamente necesario pero no causa problemas.
# Si estás en Jupyter Notebook, descomenta la siguiente línea:
# %matplotlib inline

print("=" * 70)
print("  ✅ Todas las librerías fueron importadas correctamente.")
print("=" * 70)

# --- 1.2 Lectura del archivo CSV ---

# Usamos pd.read_csv() para leer el archivo CSV y cargarlo en un DataFrame.
# Un DataFrame es como una tabla de Excel dentro de Python: tiene filas, columnas,
# y cada columna puede tener un tipo de dato diferente (texto, número, fecha, etc.).
# NOTA: Asegúrate de que el archivo 'base_datos_restaurantes_USA_v2.csv' esté
# en la misma carpeta que este notebook, o escribe la ruta completa del archivo.
df_original = pd.read_csv("base_datos_restaurantes_USA_v2.csv")

# Creamos una COPIA del DataFrame original. Esto es MUY IMPORTANTE porque
# durante la limpieza modificaremos los datos, y necesitamos conservar el
# DataFrame original intacto para poder comparar el "antes" y "después"
# (por ejemplo, en los boxplots comparativos de la sección de gráficos).
# .copy() crea una copia independiente; sin él, ambas variables apuntarían
# a los mismos datos en memoria y los cambios en uno afectarían al otro.
df = df_original.copy()

print("✅ Archivo CSV cargado exitosamente.")
print(f"   El dataset tiene {df.shape[0]} filas (registros) y {df.shape[1]} columnas (variables).\n")

# --- 1.3 Exploración inicial de los datos ---

# .head() muestra las primeras 5 filas del DataFrame por defecto.
# Es la primera función que SIEMPRE debemos usar al cargar datos nuevos.
# Nos permite ver rápidamente: los nombres de las columnas, el tipo de datos
# que contienen, y si hay valores que parecen extraños a simple vista.
print("=" * 70)
print("📋 PRIMERAS 5 FILAS DEL DATASET (head):")
print("=" * 70)
print(df.head())
print()

# .info() nos da un resumen técnico completo del DataFrame:
# - Cuántas filas y columnas tiene
# - El nombre de cada columna
# - Cuántos valores NO nulos tiene cada columna (los que sí tienen dato)
# - El tipo de dato de cada columna (int64=entero, float64=decimal, object=texto)
# - Cuánta memoria ocupa el DataFrame en RAM
# Esto es crucial para detectar columnas con datos faltantes (nulos).
print("=" * 70)
print("ℹ️  INFORMACIÓN GENERAL DEL DATASET (info):")
print("=" * 70)
df.info()
print()

# .describe() calcula estadísticas descriptivas automáticas SOLO para las
# columnas numéricas: count (cantidad de datos no nulos), mean (promedio),
# std (desviación estándar), min (mínimo), 25% (cuartil 1), 50% (mediana),
# 75% (cuartil 3), max (máximo).
# Es fundamental para detectar anomalías: por ejemplo, si la edad tiene
# un mínimo de -5 o un máximo de 300, algo está mal.
print("=" * 70)
print("📊 RESUMEN ESTADÍSTICO DE VARIABLES NUMÉRICAS (describe):")
print("=" * 70)
print(df.describe())
print()

# Verificamos cuántos valores nulos hay en CADA columna.
# .isnull() convierte cada celda en True (si es nulo) o False (si tiene valor).
# .sum() cuenta cuántos True hay por columna, dándonos el total de nulos.
# Esto nos dice exactamente dónde debemos enfocar la limpieza de datos.
print("=" * 70)
print("🔍 CONTEO DE VALORES NULOS POR COLUMNA:")
print("=" * 70)
print(df.isnull().sum())
print()


# =============================================================================
# ████████████ BLOQUE 2: LIMPIEZA DE DATOS ████████████████████████████████████
# =============================================================================
# La limpieza de datos es el paso MÁS IMPORTANTE en cualquier análisis.
# "Basura entra, basura sale": si los datos están sucios, nuestras
# conclusiones serán incorrectas. En este bloque:
# 1. Eliminamos duplicados
# 2. Tratamos edades incoherentes
# 3. Rellenamos variables cualitativas nulas
# 4. Tratamos correos electrónicos faltantes
# =============================================================================

print("\n" + "=" * 70)
print("🧹 INICIANDO LIMPIEZA DE DATOS...")
print("=" * 70)

# --- 2.1 Eliminación de duplicados ---

# Verificamos si existen registros duplicados basándonos en 'id_persona'.
# Cada persona debería tener un ID único. Si hay duplicados, significa que
# el mismo cliente aparece más de una vez, lo cual distorsionaría nuestros
# cálculos (conteos, promedios, etc.).
# .duplicated(subset='id_persona') marca como True las filas cuyo id_persona
# ya apareció antes. .sum() cuenta cuántos duplicados hay.
duplicados_antes = df.duplicated(subset='id_persona').sum()
print(f"\n🔄 Registros duplicados encontrados (por id_persona): {duplicados_antes}")

# .drop_duplicates() elimina las filas duplicadas.
# - subset='id_persona': solo busca duplicados en esta columna.
# - keep='first': conserva la PRIMERA aparición y elimina las siguientes.
# - inplace=True: modifica el DataFrame directamente en lugar de crear uno nuevo.
#   Es equivalente a hacer: df = df.drop_duplicates(...)
df.drop_duplicates(subset='id_persona', keep='first', inplace=True)

# Verificamos que los duplicados fueron eliminados correctamente.
duplicados_despues = df.duplicated(subset='id_persona').sum()
print(f"   Registros duplicados después de limpiar: {duplicados_despues}")
print(f"   ✅ Registros restantes: {df.shape[0]}")

# --- 2.2 Tratamiento de la variable 'edad' ---

# PROBLEMA: La edad tiene valores incoherentes. En el .describe() vimos que
# el mínimo es -5 (nadie tiene edad negativa) y el máximo es 300 (nadie vive
# tanto). Necesitamos identificar y corregir estos datos.

# Paso 2.2.1: Creamos una columna temporal llamada 'rango_edad' para
# CATEGORIZAR cada edad en grupos y así visualizar mejor qué valores son válidos.
# pd.cut() divide un rango numérico continuo en intervalos (bins) discretos.
# - bins: los límites de los intervalos. Por ejemplo, (0, 18] significa "de 0 a 18".
# - labels: las etiquetas descriptivas para cada intervalo.
# - right=True: incluye el límite derecho del intervalo (ej: 18 entra en "Joven").
# Los valores que NO caen en ningún intervalo (como -5 o 300) quedarán como NaN.
bins = [-float('inf'), 0, 18, 35, 50, 65, 100, float('inf')]
labels = ['Negativo (inválido)', 'Joven (0-18)', 'Adulto joven (19-35)',
          'Adulto (36-50)', 'Adulto mayor (51-65)', 'Tercera edad (66-100)',
          'Excesivo (inválido)']

df['rango_edad'] = pd.cut(df['edad'], bins=bins, labels=labels, right=True)

# Mostramos cuántas personas caen en cada categoría de edad.
# .value_counts() cuenta cuántas veces aparece cada categoría.
# dropna=False incluye los NaN en el conteo (edades que ya eran nulas).
print("\n📊 Distribución de edades por categoría:")
print(df['rango_edad'].value_counts(dropna=False))

# Paso 2.2.2: Convertimos a NaN los valores de edad que son INCOHERENTES.
# Definimos como "incoherente" toda edad que sea menor a 0 O mayor a 100.
# Estas edades son imposibles en la realidad y deben tratarse como datos faltantes.
# El operador | significa "O" (OR lógico): basta con que se cumpla UNA condición.
# .loc[condición, 'columna'] = valor: modifica SOLO las filas que cumplen la condición.
# np.nan es el valor especial "Not a Number" de NumPy, que Pandas entiende como "vacío".
edades_invalidas = ((df['edad'] < 0) | (df['edad'] > 100)).sum()
print(f"\n⚠️  Edades incoherentes detectadas (< 0 o > 100): {edades_invalidas}")

df.loc[(df['edad'] < 0) | (df['edad'] > 100), 'edad'] = np.nan

print(f"   Valores nulos en 'edad' después de invalidar: {df['edad'].isnull().sum()}")

# Paso 2.2.3: Rellenamos las edades nulas con el PROMEDIO de edad agrupado
# por la variable 'consume_licor'. ¿Por qué agrupamos por 'consume_licor'?
# Porque el consumo de licor está correlacionado con la edad (los menores de edad
# normalmente no consumen licor). Así, si una persona que SÍ consume licor tiene
# edad faltante, le asignamos el promedio de quienes SÍ consumen, y viceversa.
# Esto produce un valor más representativo que simplemente usar el promedio general.

# Calculamos el promedio de edad POR GRUPO de 'consume_licor'.
# .groupby('consume_licor') agrupa los datos por los valores únicos de esa columna.
# ['edad'].mean() calcula el promedio de edad dentro de cada grupo.
promedio_edad_por_licor = df.groupby('consume_licor')['edad'].mean()
print(f"\n📈 Promedio de edad por grupo de 'consume_licor':")
print(promedio_edad_por_licor)

# .transform() aplica una función a cada grupo y devuelve un resultado del MISMO
# tamaño que el DataFrame original (una fila por cada fila original).
# A diferencia de .agg() que devuelve un resumen, .transform() "propaga" el
# resultado grupal a cada fila de ese grupo. Esto nos permite rellenar cada
# fila faltante con el promedio de SU grupo específico.
# .fillna() reemplaza los NaN con el valor proporcionado.
# .round(0) redondea al entero más cercano (la edad debe ser un número entero).
df['edad'] = df['edad'].fillna(
    df.groupby('consume_licor')['edad'].transform('mean')
).round(0)

print(f"   Valores nulos en 'edad' después de rellenar: {df['edad'].isnull().sum()}")
print("   ✅ Edad limpia y completa.")

# --- 2.3 Tratamiento de variables cualitativas ---

# PROBLEMA: La columna 'preferencias_alimenticias' tiene valores nulos (1403).
# Para las variables cualitativas (categóricas, de texto), NO podemos usar el
# promedio (no existe "promedio" de textos como "Carnes" y "Vegano").
# En su lugar, usamos la MODA: el valor más frecuente.
# Además, lo hacemos agrupado por 'ciudad_residencia', porque las preferencias
# alimenticias pueden variar según la ciudad (ej: más mariscos en ciudades costeras).

print(f"\n🍽️  Nulos en 'preferencias_alimenticias' antes de limpiar: "
      f"{df['preferencias_alimenticias'].isnull().sum()}")

# Definimos una función que, para cada grupo (ciudad), encuentra la moda y rellena
# los nulos con ese valor.
# .mode()[0] obtiene el valor más frecuente (moda). El [0] es porque .mode()
# puede devolver múltiples modas si hay empate; tomamos la primera.
# .fillna() reemplaza solo los NaN dejando intactos los valores existentes.

# ESTRATEGIA: En lugar de usar groupby().apply() (que puede consumir la columna
# de agrupación como índice y perderla), usamos un enfoque más seguro:
# 1. Calculamos la moda de 'preferencias_alimenticias' por ciudad.
# 2. Mapeamos esa moda a cada fila según su ciudad.
# 3. Rellenamos los nulos con el valor mapeado.

# Paso 1: Calculamos la moda (valor más frecuente) de 'preferencias_alimenticias'
# para CADA ciudad. .groupby() agrupa por ciudad, luego .agg() aplica una función
# personalizada: si hay al menos una moda, tomamos la primera (iloc[0]).
moda_por_ciudad = df.groupby('ciudad_residencia')['preferencias_alimenticias'].agg(
    lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan
)

# Mostramos la moda por ciudad para verificar:
print("\n   Moda de preferencia alimenticia por ciudad:")
print(moda_por_ciudad)

# Paso 2: .map() busca el valor de moda correspondiente a la ciudad de cada fila.
# Para cada fila, toma su 'ciudad_residencia' y busca en moda_por_ciudad
# cuál es la moda de esa ciudad. El resultado es una Serie con el valor de
# relleno apropiado para cada fila (basado en su ciudad).
valores_de_relleno = df['ciudad_residencia'].map(moda_por_ciudad)

# Paso 3: .fillna() reemplaza SOLO los NaN en 'preferencias_alimenticias'
# con el valor correspondiente de valores_de_relleno. Los valores existentes
# (no nulos) se mantienen intactos.
df['preferencias_alimenticias'] = df['preferencias_alimenticias'].fillna(valores_de_relleno)

print(f"   Nulos en 'preferencias_alimenticias' después de limpiar: "
      f"{df['preferencias_alimenticias'].isnull().sum()}")
print("   ✅ Preferencias alimenticias completas.")

# --- 2.4 Tratamiento de la columna 'correo_electronico' ---

# Los correos electrónicos faltantes se rellenan con el texto "NA" (Not Available).
# .fillna("NA") reemplaza todos los NaN en esa columna por la cadena de texto "NA".
# Esto es útil porque al exportar a CSV, los campos vacíos pueden causar problemas
# en otros programas. Con "NA" queda claro que el dato no está disponible.
print(f"\n📧 Nulos en 'correo_electronico' antes de limpiar: "
      f"{df['correo_electronico'].isnull().sum()}")

df['correo_electronico'] = df['correo_electronico'].fillna("NA")

print(f"   Nulos en 'correo_electronico' después de limpiar: "
      f"{df['correo_electronico'].isnull().sum()}")
print("   ✅ Correos electrónicos completos.")

# --- 2.5 Eliminación de columnas temporales ---

# Durante el proceso de limpieza creamos la columna temporal 'rango_edad'
# que sirvió para diagnosticar los datos incoherentes. Ya no la necesitamos,
# así que la eliminamos para dejar el DataFrame limpio y profesional.
# .drop() elimina filas o columnas.
# - columns=['rango_edad']: especifica qué columna(s) eliminar.
# - inplace=True: modifica el DataFrame directamente.
df.drop(columns=['rango_edad'], inplace=True)

print("\n🗑️  Columna temporal 'rango_edad' eliminada.")

# --- 2.6 Guardado del DataFrame limpio ---

# Exportamos el DataFrame limpio a un nuevo archivo CSV llamado 'clientes_final.csv'.
# .to_csv() convierte el DataFrame a formato CSV y lo guarda en disco.
# - index=False: NO incluye el índice numérico de Python como columna en el CSV.
#   Si pusiéramos True (o lo omitiéramos), se añadiría una columna extra con
#   números 0, 1, 2... que no son parte de nuestros datos originales.
df.to_csv("clientes_final.csv", index=False)

print(f"\n💾 DataFrame limpio guardado como 'clientes_final.csv'")
print(f"   Registros finales: {df.shape[0]} filas x {df.shape[1]} columnas")

# Verificación final: mostramos el conteo de nulos restantes.
print("\n" + "=" * 70)
print("🔍 VERIFICACIÓN FINAL - NULOS RESTANTES:")
print("=" * 70)
print(df.isnull().sum())
print()


# =============================================================================
# ████████████ BLOQUE 3: ESTADÍSTICOS DE COMPARACIÓN █████████████████████████
# =============================================================================
# En este bloque creamos funciones reutilizables para calcular estadísticas
# de comparación entre grupos. Las funciones nos permiten automatizar cálculos
# que queremos repetir con diferentes variables sin reescribir el código.
# =============================================================================

# Leemos la base de datos LIMPIA para asegurarnos de trabajar con datos correctos.
# Aunque ya tenemos 'df' en memoria, esta línea garantiza que si ejecutamos
# este bloque de forma independiente, siempre usará el archivo limpio.
df_limpio = pd.read_csv("clientes_final.csv")

print("\n" + "=" * 70)
print("📊 ESTADÍSTICOS DE COMPARACIÓN")
print("=" * 70)

# --- 3.1 Función calcular_promedio ---

def calcular_promedio(df, columna_grupo):
    """
    Calcula el promedio de las principales variables numéricas agrupadas
    por una columna categórica del DataFrame.

    Parámetros:
    -----------
    df : pandas.DataFrame
        El DataFrame con los datos a analizar. Debe contener las columnas:
        'edad', 'frecuencia_visita', 'promedio_gasto_comida' e 'ingresos_mensuales'.
    columna_grupo : str
        Nombre de la columna categórica por la cual se agruparán los datos.
        Por ejemplo: 'ciudad_residencia', 'genero', 'estrato_socioeconomico'.

    Retorna:
    --------
    pandas.DataFrame
        Una tabla donde cada fila es un grupo (valor único de columna_grupo)
        y cada columna es el promedio de la variable numérica correspondiente.

    Ejemplo de uso:
    ---------------
    >>> resultado = calcular_promedio(df_limpio, 'ciudad_residencia')
    >>> print(resultado)
    """
    # Definimos las columnas numéricas de las cuales queremos el promedio.
    # Estas son las variables que el enunciado del taller nos pide analizar.
    columnas_numericas = ['edad', 'frecuencia_visita',
                          'promedio_gasto_comida', 'ingresos_mensuales']

    # .groupby(columna_grupo) agrupa los datos por los valores únicos de esa columna.
    # [columnas_numericas] selecciona SOLO las columnas numéricas que nos interesan.
    # .mean() calcula el promedio de cada columna dentro de cada grupo.
    # .round(2) redondea a 2 decimales para mejor legibilidad.
    resultado = df.groupby(columna_grupo)[columnas_numericas].mean().round(2)

    return resultado


# DEMOSTRACIÓN: Calculamos promedios agrupados por ciudad de residencia.
print("\n📈 Promedio de variables numéricas POR CIUDAD:")
print("-" * 70)
promedios_ciudad = calcular_promedio(df_limpio, 'ciudad_residencia')
print(promedios_ciudad)

# DEMOSTRACIÓN: Calculamos promedios agrupados por género.
print("\n📈 Promedio de variables numéricas POR GÉNERO:")
print("-" * 70)
promedios_genero = calcular_promedio(df_limpio, 'genero')
print(promedios_genero)


# --- 3.2 Función tabla_cruzada ---

def tabla_cruzada(df, col_filas, col_columnas):
    """
    Genera una tabla cruzada (de contingencia) entre dos variables categóricas,
    mostrando los PORCENTAJES por fila. Esto permite analizar la relación
    entre dos variables cualitativas.

    Una tabla cruzada muestra cómo se distribuye una variable en relación
    con otra. Por ejemplo: ¿qué porcentaje de los clientes en Miami son
    hombres vs mujeres?

    Parámetros:
    -----------
    df : pandas.DataFrame
        El DataFrame con los datos a analizar.
    col_filas : str
        Nombre de la columna que irá en las FILAS de la tabla.
        Ejemplo: 'ciudad_residencia'.
    col_columnas : str
        Nombre de la columna que irá en las COLUMNAS de la tabla.
        Ejemplo: 'genero'.

    Retorna:
    --------
    pandas.DataFrame
        Una tabla cruzada con porcentajes por fila (cada fila suma 100%).

    Ejemplo de uso:
    ---------------
    >>> tabla = tabla_cruzada(df_limpio, 'ciudad_residencia', 'genero')
    >>> print(tabla)
    """
    # pd.crosstab() crea automáticamente una tabla cruzada.
    # - df[col_filas]: la variable que va en las filas.
    # - df[col_columnas]: la variable que va en las columnas.
    # - normalize='index': normaliza POR FILA, es decir, cada fila sumará 1.0 (100%).
    #   Otras opciones: 'columns' (normaliza por columna), 'all' (normaliza por total).
    # * 100: convertimos las proporciones (0.0 a 1.0) a porcentajes (0% a 100%).
    # .round(2): redondeamos a 2 decimales para legibilidad.
    tabla = pd.crosstab(df[col_filas], df[col_columnas], normalize='index') * 100
    tabla = tabla.round(2)

    return tabla


# DEMOSTRACIÓN: Tabla cruzada de ciudad de residencia vs género.
print("\n📊 Tabla Cruzada: Ciudad de Residencia vs Género (% por fila):")
print("-" * 70)
tabla_ciudad_genero = tabla_cruzada(df_limpio, 'ciudad_residencia', 'genero')
print(tabla_ciudad_genero)

# DEMOSTRACIÓN: Tabla cruzada de ciudad de residencia vs preferencias alimenticias.
print("\n📊 Tabla Cruzada: Ciudad vs Preferencias Alimenticias (% por fila):")
print("-" * 70)
tabla_ciudad_pref = tabla_cruzada(df_limpio, 'ciudad_residencia', 'preferencias_alimenticias')
print(tabla_ciudad_pref)


# =============================================================================
# ████████████ BLOQUE 4: GRÁFICOS Y ANÁLISIS VISUAL ██████████████████████████
# =============================================================================
# La visualización de datos es esencial para comunicar hallazgos de forma
# clara e intuitiva. Un buen gráfico puede transmitir en segundos lo que
# una tabla de números tardaría minutos en explicar.
# =============================================================================

print("\n" + "=" * 70)
print("📊 GENERANDO GRÁFICOS...")
print("=" * 70)

# --- 4.1 Diagrama de Barras: Cantidad de clientes por ciudad ---

# Este gráfico muestra cuántos clientes hay en cada ciudad.
# Es un gráfico de barras (bar chart), ideal para comparar cantidades
# entre categorías (en este caso, ciudades).

# plt.figure() crea una nueva "figura" (lienzo) para dibujar el gráfico.
# figsize=(12, 6) define el tamaño: 12 pulgadas de ancho x 6 de alto.
# Esto asegura que el gráfico sea lo suficientemente grande para ser legible.
plt.figure(figsize=(12, 6))

# sns.countplot() de Seaborn crea un gráfico de barras que CUENTA
# automáticamente cuántas veces aparece cada valor único en la variable.
# - data=df_limpio: el DataFrame del cual tomar los datos.
# - x='ciudad_residencia': la variable categórica a contar.
# - palette='viridis': paleta de colores profesional (verde-amarillo-morado).
# - order=...: ordenamos las barras de mayor a menor para facilitar la comparación.
#   .value_counts().index devuelve las ciudades ordenadas por frecuencia descendente.
ax = sns.countplot(data=df_limpio, x='ciudad_residencia',
                   hue='ciudad_residencia', palette='viridis', legend=False,
                   order=df_limpio['ciudad_residencia'].value_counts().index)

# plt.title() establece el título del gráfico.
# fontsize=14 define el tamaño de la fuente. fontweight='bold' lo pone en negrilla.
plt.title('Cantidad de Clientes por Ciudad de Residencia',
          fontsize=14, fontweight='bold')

# plt.xlabel() y plt.ylabel() etiquetan los ejes X e Y respectivamente.
# Siempre debemos etiquetar los ejes para que el gráfico sea autoexplicativo.
plt.xlabel('Ciudad de Residencia', fontsize=12)
plt.ylabel('Cantidad de Clientes', fontsize=12)

# plt.xticks(rotation=45) rota las etiquetas del eje X a 45 grados.
# Esto evita que los nombres de las ciudades se sobrepongan entre sí.
# ha='right' alinea las etiquetas a la derecha para mejor lectura.
plt.xticks(rotation=45, ha='right')

# Añadimos el valor numérico exacto encima de cada barra para mayor precisión.
# ax.patches contiene cada barra del gráfico como un objeto.
# .get_height() obtiene la altura de la barra (el conteo).
# ax.text() escribe texto en una posición específica del gráfico.
for barra in ax.patches:
    ax.text(barra.get_x() + barra.get_width() / 2.,   # Posición X: centro de la barra
            barra.get_height() + 50,                     # Posición Y: justo arriba de la barra
            f'{int(barra.get_height())}',                # Texto: el conteo como entero
            ha='center', va='bottom', fontsize=10)       # Centrado horizontalmente

# plt.tight_layout() ajusta automáticamente los márgenes del gráfico
# para que nada se corte o se superponga. Siempre es buena práctica usarlo.
plt.tight_layout()

# plt.savefig() guarda el gráfico como imagen PNG en disco.
# dpi=150 define la resolución (puntos por pulgada); 150 es buena para informes.
# bbox_inches='tight' recorta los espacios blancos innecesarios alrededor.
plt.savefig("grafico_barras_clientes_por_ciudad.png", dpi=150, bbox_inches='tight')

# plt.show() muestra el gráfico en pantalla (en el notebook).
plt.show()

print("✅ Gráfico de barras guardado como 'grafico_barras_clientes_por_ciudad.png'\n")


# --- 4.2 Diagramas de Bigotes (Boxplots) Comparativos de Edad ---

# Los boxplots (diagramas de caja y bigotes) son EXCELENTES para:
# 1. Ver la distribución central de los datos (mediana, cuartiles).
# 2. Detectar VALORES ATÍPICOS (outliers) representados como puntos aislados.
# 3. Comparar distribuciones entre grupos.
#
# Aquí creamos DOS boxplots lado a lado:
# - Izquierda: edad con datos ORIGINALES (antes de limpiar) → se verán outliers extremos.
# - Derecha: edad con datos LIMPIOS (después de limpiar) → distribución más saludable.
# Esto demuestra visualmente el impacto positivo de nuestra limpieza de datos.

# plt.subplots() crea una figura con múltiples subgráficos (subplots).
# nrows=1, ncols=2: 1 fila y 2 columnas = 2 gráficos lado a lado.
# figsize=(14, 6): tamaño total de la figura.
# fig es el objeto "figura" completo; axes es un array con los dos ejes.
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

# --- Boxplot IZQUIERDO: Datos originales (ANTES de limpiar) ---
# axes[0] se refiere al primer subgráfico (izquierda).
# sns.boxplot() crea el boxplot.
# - y=df_original['edad']: graficamos la edad del DataFrame ORIGINAL (sin limpiar).
# - ax=axes[0]: dibujamos en el primer subgráfico.
# - color='salmon': color rosa-anaranjado para distinguirlo.
# - flierprops: personaliza la apariencia de los outliers (puntos rojos).
sns.boxplot(y=df_original['edad'], ax=axes[0], color='salmon',
            flierprops=dict(marker='o', markerfacecolor='red', markersize=4))
axes[0].set_title('Edad - ANTES de Limpiar\n(Datos Originales)',
                  fontsize=13, fontweight='bold')
axes[0].set_ylabel('Edad', fontsize=12)

# --- Boxplot DERECHO: Datos limpios (DESPUÉS de limpiar) ---
# axes[1] se refiere al segundo subgráfico (derecha).
# Usamos df_limpio que ya tiene las edades corregidas.
# - color='lightgreen': color verde claro para indicar "datos saludables".
sns.boxplot(y=df_limpio['edad'], ax=axes[1], color='lightgreen',
            flierprops=dict(marker='o', markerfacecolor='green', markersize=4))
axes[1].set_title('Edad - DESPUÉS de Limpiar\n(Datos Corregidos)',
                  fontsize=13, fontweight='bold')
axes[1].set_ylabel('Edad', fontsize=12)

# plt.suptitle() añade un título general que abarca TODA la figura (los dos gráficos).
plt.suptitle('Comparación de la Distribución de Edad: Antes vs Después de la Limpieza',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig("grafico_boxplots_edad_comparativo.png", dpi=150, bbox_inches='tight')
plt.show()

print("✅ Boxplots comparativos guardados como 'grafico_boxplots_edad_comparativo.png'\n")


# --- 4.3 Diagrama de Torta (Pie Chart): Proporción de clientes por género ---

# El diagrama de torta (pie chart) muestra proporciones como "tajadas" de un
# círculo. Es ideal cuando queremos ver qué porcentaje del total representa
# cada categoría. Aquí lo usamos para visualizar la distribución por género.

# .value_counts() cuenta cuántas veces aparece cada género.
conteo_genero = df_limpio['genero'].value_counts()

# Creamos la figura para el gráfico de torta.
plt.figure(figsize=(8, 8))

# plt.pie() crea el diagrama de torta.
# - conteo_genero.values: los valores numéricos (conteos) para cada tajada.
# - labels: las etiquetas de cada tajada (los nombres de los géneros).
# - autopct='%1.1f%%': muestra el porcentaje dentro de cada tajada.
#   %1.1f significa: 1 dígito antes del punto, 1 después. %% imprime el símbolo %.
# - startangle=90: inicia la primera tajada a las 12 en punto (90°).
# - colors: colores personalizados para cada tajada.
# - explode: separa ligeramente una tajada del centro para destacarla.
#   (0.03, 0.03) significa una separación mínima uniforme.
# - shadow=True: añade una sombra sutil para efecto 3D.
# - textprops: propiedades del texto (tamaño de fuente).
colores_genero = ['#FF6B6B', '#4ECDC4']  # Rojo coral y turquesa
explode_genero = (0.03, 0.03)            # Ligera separación entre tajadas

plt.pie(conteo_genero.values,
        labels=conteo_genero.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colores_genero,
        explode=explode_genero,
        shadow=True,
        textprops={'fontsize': 13})

plt.title('Proporción de Clientes por Género',
          fontsize=14, fontweight='bold', pad=20)

# plt.axis('equal') asegura que el círculo se dibuje como un círculo perfecto
# y no como una elipse (puede ocurrir si la figura no es cuadrada).
plt.axis('equal')

plt.tight_layout()
plt.savefig("grafico_torta_genero.png", dpi=150, bbox_inches='tight')
plt.show()

print("✅ Diagrama de torta (género) guardado como 'grafico_torta_genero.png'\n")

# --- Diagrama de Torta ADICIONAL: Preferencias Alimenticias ---

# Creamos un segundo diagrama de torta para las preferencias alimenticias.
# Esto nos permite ver qué tipo de comida prefieren los clientes en general.
conteo_preferencias = df_limpio['preferencias_alimenticias'].value_counts()

plt.figure(figsize=(9, 9))

# Paleta de colores más amplia porque hay más categorías (6 preferencias).
colores_pref = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
explode_pref = tuple([0.03] * len(conteo_preferencias))  # Separación uniforme

plt.pie(conteo_preferencias.values,
        labels=conteo_preferencias.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colores_pref,
        explode=explode_pref,
        shadow=True,
        textprops={'fontsize': 12})

plt.title('Proporción de Clientes por Preferencia Alimenticia',
          fontsize=14, fontweight='bold', pad=20)

plt.axis('equal')
plt.tight_layout()
plt.savefig("grafico_torta_preferencias.png", dpi=150, bbox_inches='tight')
plt.show()

print("✅ Diagrama de torta (preferencias) guardado como 'grafico_torta_preferencias.png'\n")


# --- 4.4 Histograma: Distribución de Ingresos Mensuales ---

# Un histograma divide los valores numéricos en intervalos (bins) y cuenta
# cuántas observaciones caen en cada intervalo. Es la forma más usada para
# visualizar la DISTRIBUCIÓN de una variable numérica continua.
# Nos permite ver: si los datos son simétricos, si tienen sesgo, si hay
# concentraciones en ciertos rangos, etc.

plt.figure(figsize=(12, 6))

# sns.histplot() de Seaborn crea un histograma mejorado.
# - data=df_limpio: el DataFrame fuente.
# - x='ingresos_mensuales': la variable numérica a graficar.
# - bins=30: divide el rango de datos en 30 intervalos iguales.
#   Más bins = más detalle, menos bins = vista más general.
# - kde=True: superpone una Curva de Densidad de Kernel (KDE).
#   Esta curva suaviza el histograma para mostrar la forma general de la
#   distribución como una línea continua. Es muy útil para identificar
#   la forma de la distribución (normal, sesgada, bimodal, etc.).
# - color='steelblue': color azul acero para las barras.
# - edgecolor='white': borde blanco entre barras para mejor separación visual.
sns.histplot(data=df_limpio, x='ingresos_mensuales', bins=30,
             kde=True, color='steelblue', edgecolor='white')

plt.title('Distribución de Ingresos Mensuales de los Clientes',
          fontsize=14, fontweight='bold')
plt.xlabel('Ingresos Mensuales (USD)', fontsize=12)
plt.ylabel('Frecuencia (Cantidad de Clientes)', fontsize=12)

# Añadimos una línea vertical en la media (promedio) de los ingresos.
# plt.axvline() dibuja una línea vertical en la posición especificada.
# - x=media: posición en el eje X donde se dibuja la línea.
# - color='red': la línea será roja para que destaque.
# - linestyle='--': estilo de línea punteada (dashed).
# - linewidth=2: grosor de la línea.
# - label: texto para la leyenda del gráfico.
media_ingresos = df_limpio['ingresos_mensuales'].mean()
mediana_ingresos = df_limpio['ingresos_mensuales'].median()

plt.axvline(x=media_ingresos, color='red', linestyle='--', linewidth=2,
            label=f'Media: ${media_ingresos:,.0f}')
plt.axvline(x=mediana_ingresos, color='orange', linestyle='-.', linewidth=2,
            label=f'Mediana: ${mediana_ingresos:,.0f}')

# plt.legend() muestra la leyenda con las etiquetas que definimos arriba.
# fontsize=11 define el tamaño de texto de la leyenda.
plt.legend(fontsize=11)

plt.tight_layout()
plt.savefig("grafico_histograma_ingresos.png", dpi=150, bbox_inches='tight')
plt.show()

print("✅ Histograma de ingresos guardado como 'grafico_histograma_ingresos.png'\n")


# --- Histograma ADICIONAL: Distribución del Gasto Promedio en Comida ---

# Creamos un segundo histograma para el gasto en comida, ya que el enunciado
# menciona esta variable como opción. Así el taller queda más completo.

plt.figure(figsize=(12, 6))

sns.histplot(data=df_limpio, x='promedio_gasto_comida', bins=30,
             kde=True, color='#2ecc71', edgecolor='white')

plt.title('Distribución del Gasto Promedio en Comida por Visita',
          fontsize=14, fontweight='bold')
plt.xlabel('Gasto Promedio en Comida (USD)', fontsize=12)
plt.ylabel('Frecuencia (Cantidad de Clientes)', fontsize=12)

# Líneas de referencia para media y mediana del gasto en comida.
media_gasto = df_limpio['promedio_gasto_comida'].mean()
mediana_gasto = df_limpio['promedio_gasto_comida'].median()

plt.axvline(x=media_gasto, color='red', linestyle='--', linewidth=2,
            label=f'Media: ${media_gasto:,.2f}')
plt.axvline(x=mediana_gasto, color='orange', linestyle='-.', linewidth=2,
            label=f'Mediana: ${mediana_gasto:,.2f}')

plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig("grafico_histograma_gasto_comida.png", dpi=150, bbox_inches='tight')
plt.show()

print("✅ Histograma de gasto en comida guardado como 'grafico_histograma_gasto_comida.png'\n")


# =============================================================================
# ████████████ RESUMEN FINAL █████████████████████████████████████████████████
# =============================================================================

print("\n" + "=" * 70)
print("🏆 RESUMEN DEL PROCESO COMPLETADO:")
print("=" * 70)
print(f"""
📁 Archivos generados:
   1. clientes_final.csv              → Base de datos limpia
   2. grafico_barras_clientes_por_ciudad.png  → Barras por ciudad
   3. grafico_boxplots_edad_comparativo.png   → Boxplots antes/después
   4. grafico_torta_genero.png                → Torta de género
   5. grafico_torta_preferencias.png          → Torta de preferencias
   6. grafico_histograma_ingresos.png         → Histograma de ingresos
   7. grafico_histograma_gasto_comida.png     → Histograma de gasto

📊 Funciones creadas:
   • calcular_promedio(df, columna_grupo) → Promedios por grupo
   • tabla_cruzada(df, col_filas, col_columnas) → Tabla cruzada con %

🧹 Limpieza realizada:
   • Duplicados eliminados por id_persona
   • Edades incoherentes (<0 o >100) convertidas a NaN y rellenadas
     con el promedio agrupado por consume_licor
   • Preferencias alimenticias nulas rellenadas con la moda por ciudad
   • Correos electrónicos nulos rellenados con "NA"
   • Columnas temporales eliminadas
""")
print("=" * 70)
print("✅ ¡Análisis completado exitosamente!")
print("=" * 70)
