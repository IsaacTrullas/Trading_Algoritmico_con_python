''' 2.1.1'''
# Variables y Tipos de Datos:
precio_accion = 150.50  # Esto es un número decimal
cantidad = 10  # Esto es un número entero
activo = "AAPL"  # Esto es una cadena de texto
es_rentable = True  # Esto es un valor booleano

print(type(precio_accion))  # Salida: <class 'float'>

# Condicionales:
if precio_accion > 100:
    print("El precio es alto")
elif precio_accion > 50:
    print("El precio es moderado")
else:
    print("El precio es bajo")

# Bucles:
# bucle for:
precios_historicos = [150, 155, 160, 158, 165]

for precio in precios_historicos:
    print(f"El precio actual es: {precio}")

# bucle while:
precio_actual = 90
while precio_actual < 100:
    precio_actual += 1  # Simula el aumento del precio
    print(f"Esperando a que el precio supere los 100: {precio_actual}")

''' 2.1.2'''
# Listas en Python
# Creación y Acceso a Elementos:
precios_acciones = [100, 105, 110, 115, 120]
print(precios_acciones[0])  # Imprime el primer elemento: 100
print(precios_acciones[-1])  # Imprime el último elemento: 120

# Agregar y Eliminar Elementos:
precios_acciones.append(125)  # Añade un nuevo elemento al final de la lista
print(precios_acciones)  # [100, 105, 110, 115, 120, 125]

precios_acciones.remove(105)  # Elimina el primer elemento que coincida con el valor
print(precios_acciones)  # [100, 110, 115, 120, 125]

# Slicing (Corte de Listas):
primeros_tres = precios_acciones[:3]  # Obtiene los primeros tres elementos
print(primeros_tres)  # [100, 110, 115]

ultimos_dos = precios_acciones[-2:]  # Obtiene los dos últimos elementos
print(ultimos_dos)  # [120, 125]

# List Comprehensions:
# Incrementa cada precio en un 5%
precios_actualizados = [precio * 1.05 for precio in precios_acciones]
print(precios_actualizados)  # [105.0, 115.5, 120.75, 126.0, 131.25]

# Diccionarios en Python
# Creación y Acceso a Elementos:
precios_acciones = {'AAPL': 150, 'GOOG': 1200, 'TSLA': 700}
print(precios_acciones['AAPL'])  # Imprime el valor asociado a 'AAPL': 150

# Agregar y Eliminar Elementos:
precios_acciones['AMZN'] = 3300  # Añade un nuevo par clave-valor
print(precios_acciones)  # {'AAPL': 150, 'GOOG': 1200, 'TSLA': 700, 'AMZN': 3300}

del precios_acciones['TSLA']  # Elimina la clave 'TSLA' y su valor asociado
print(precios_acciones)  # {'AAPL': 150, 'GOOG': 1200, 'AMZN': 3300}

# Iterar sobre Diccionarios:
for clave, valor in precios_acciones.items():
    print(f"El precio de {clave} es {valor}")

# Comprensiones de Diccionarios:
# Incrementa cada precio en un 10%
precios_actualizados = {clave: valor * 1.10 for clave, valor in precios_acciones.items()}
print(precios_actualizados) # {'AAPL': 165.0, 'GOOG': 1320.0,'AMZN': 3630.0}

# Pandas para Análisis de Datos
# Creación de un DataFrame:
import pandas as pd

datos = {
    'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
    'AAPL': [150, 152, 151],
    'GOOG': [1200, 1215, 1220]
}
df = pd.DataFrame(datos)
print(df)

# Filtrado de Datos:
precios_altos = df[df['AAPL'] > 150]
print(precios_altos)

# Agregar Valores a un DataFrame:
df['AMZN'] = [3300, 3315, 3320]  # Añadir nueva columna con datos
print(df)

df['AMZN'] = [3300, 3315, 3320]  # Añadir nueva columna con datos
print(df)

# Eliminar Valores del DataFrame:
df = df.drop(columns=['GOOG'])
print(df)

df = df.drop(index=2)
print(df)

# Ejemplo de Cálculo de Cambio Porcentual y Media Móvil utilizando Pandas:
df['AAPL_pct_change'] = df['AAPL'].pct_change()
df['SMA_50'] = df['AAPL'].rolling(window=2).mean()  
print(df[['Date', 'AAPL', 'AAPL_pct_change', 'SMA_50']])

''' 2.1.3'''
## Funciones
# Definición y Uso de Funciones:
def calcular_rendimiento(precio_inicial, precio_final):
    rendimiento = (precio_final - precio_inicial) / precio_inicial
    return rendimiento

# Llamando a la función
rendimiento = calcular_rendimiento(100, 150)
print(f"El rendimiento es: {rendimiento}") # El rendimiento es: 0.5

# Parámetros y Retornos:
def saludo(nombre):
    return f"Hola, {nombre}!"

mensaje = saludo("Isaac")
print(mensaje)

# Funciones Lambda (Anónimas):
multiplicar = lambda x, y: x * y
resultado = multiplicar(10, 5) 
print(resultado) # 50

## Módulos
# Creación de un Módulo Propio:

# Archivo: mis_funciones.py
def calcular_media_movil(precios, periodo):
    return sum(precios[-periodo:]) / periodo

def calcular_maximo(precios):
    return max(precios)

# Archivo principal
import mis_funciones

precios = [100, 105, 110, 115, 120]
media_movil = mis_funciones.calcular_media_movil(precios, 3)
print(f"La media móvil de 3 días es: {media_movil}")

maximo = mis_funciones.calcular_maximo(precios)
print(f"El precio máximo es: {maximo}")

# Uso de Módulos Integrados y Externos:
import math

# Uso del módulo math
resultado = math.sqrt(16)
print(resultado)  # Salida: 4.0

'''2.2.1'''
# Lectura de Datos desde Fuentes Externas:
import pandas as pd

# Cargar datos desde un archivo CSV
df = pd.read_csv('precios_historicos.csv')
print(df.head())  # Muestra las primeras 5 filas del DataFrame

## Operaciones Avanzadas con DataFrames:

# Cálculo de Indicadores Técnicos:
df['SMA_20'] = df['Close'].rolling(window=20).mean()
print(df[['Date', 'Close', 'SMA_20']].tail())

# Aplicación de Funciones Personalizadas con apply():
def clasificar_rendimiento(rendimiento):
    if rendimiento > 1:
        return 'Alta'
    elif rendimiento < -1:
        return 'Baja'
    else:
        return 'Neutral'

df=pd.DataFrame() # Creamos un DataFrame vacío

# Creamos datos de ejemplo
df['Date'] = pd.date_range(start='1/1/2021', periods=10, freq='D')
df['Close'] = [100, 102, 98, 105, 95, 110, 105, 100, 98, 105]

# Calcular el rendimiento diario
df['Daily_Return'] = df['Close'].pct_change() * 100

# Aplicar la función personalizada a cada valor de la columna 'Daily_Return'
df['Rendimiento_Clasificado'] = df['Daily_Return'].apply(clasificar_rendimiento)
print(df[['Date', 'Close', 'Daily_Return', 'Rendimiento_Clasificado']].tail())

'''2.2.2'''
# Creación de Arrays y Operaciones Básicas:
import numpy as np

precios = [100, 102, 101, 103, 104]
np_precios = np.array(precios)
print(np_precios)

# Calcular el logaritmo natural de cada precio
log_precios = np.log(np_precios)
print(log_precios)

# Generación de Datos Aleatorios:
# Generar 10 números aleatorios con una distribución normal
rendimientos_simulados = np.random.normal(0, 0.01, 10) # 10 números aleatorios con media 0 y desviación estándar 0.01
print(rendimientos_simulados)

'''2.2.3'''
# matplotlib Básico:
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Close'], label='Precio de Cierre')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.title('Precio de Cierre de la Acción')
plt.legend()
plt.show()

# Visualización con seaborn:
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 5))
sns.histplot(df['Daily_Return'].dropna(), bins=20, kde=True)
plt.title('Distribución de Rendimientos Diarios')
plt.show()

'''2.2.4'''
# Implementación Básica de un Modelo de Regresión Lineal:
from sklearn.linear_model import LinearRegression
import numpy as np

# Extraer los datos para entrenamiento (eliminando filas con NaN)
df = df.dropna()
X = df[['Open']].values  # Variable independiente (precio de apertura)
y = df['Close'].values  # Variable dependiente (precio de cierre)

# Dividir los datos en conjuntos de entrenamiento y prueba
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Realizar predicciones
predicciones = modelo.predict(X_test)
print("Predicciones:", predicciones[:5])
print("Valores Reales:", y_test[:5])

# Evaluación del Modelo
from sklearn.metrics import mean_squared_error, r2_score

# Calcular el error cuadrático medio y el R2
mse = mean_squared_error(y_test, predicciones)
r2 = r2_score(y_test, predicciones)

print(f"Error Cuadrático Medio (MSE): {mse}")
print(f"Coeficiente de Determinación (R²): {r2}")
