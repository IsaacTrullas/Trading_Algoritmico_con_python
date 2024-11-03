'''3.1.1'''
# yfinance
import yfinance as yf
# Obtener datos históricos de Apple (AAPL)
datos_apple = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
print(datos_apple.head())

# Web Scraping
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Definir el ticker de Tesla
ticker = 'TSLA'

# Headers para la solicitud HTTP
headers = {
    'authority': 'stockanalysis.com',
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9',
    'referer': 'https://stockanalysis.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

# URL del estado de resultados de Tesla
url = f'https://stockanalysis.com/stocks/{ticker.lower()}/financials/'

# Realizar la solicitud GET
response = requests.get(url, headers=headers)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar la tabla que contiene el estado de resultados
    table = soup.find('table', {"class": 'w-full'})
    
    if table:
        # Extraer los datos de la tabla
        rows = table.find_all('tr')
        
        # Inicializar listas para almacenar los datos
        headers = [header.text.strip() for header in rows[0].find_all('th')]
        data = []
        
        for row in rows[1:]:
            cols = row.find_all('td')
            data.append([col.text.strip() for col in cols])
        
        # Crear un DataFrame de pandas
        df = pd.DataFrame(data, columns=headers)
        print(df.iloc[:10, :3]) # Mostrar las primeras 10 filas y 3 columnas
    else:
        print("No se encontró la tabla de resultados financieros en la página.")
else:
    print(f'Error al realizar la solicitud. Código de estado: {response.status_code}')




'''3.2.1'''
# Identificación de Valores Nulos:
import pandas as pd

# Suponiendo que df es tu DataFrame
print(df.isnull().sum())  # Muestra el número de valores nulos por columna


## Eliminación de Filas o Columnas con Valores Faltantes:

# Elimina filas con cualquier valor faltante
df = df.dropna()

# Elimina columnas con cualquier valor faltante
df = df.dropna(axis=1)



##Relleno de Valores Faltantes:

# Rellenar con la media de cada columna
df.fillna(df.mean(), inplace=True)

# Rellenar con el valor anterior (Forward Fill)
df.fillna(method='ffill', inplace=True)

# Rellenar con el valor siguiente (Backward Fill)
df.fillna(method='bfill', inplace=True)



## Interpolación de Datos Faltantes:

# Interpolación Lineal
df.interpolate(method='linear', inplace=True)

# Interpolación Polinómica
df.interpolate(method='polynomial', order=2, inplace=True)

# Interpolación Spline
df.interpolate(method='spline', order=3, inplace=True)

# Interpolación por Método de Aproximación de Valores Cercanos
df.interpolate(method='nearest', inplace=True)

# Ejemplo de Interpolación Lineal en una Serie Temporal
import pandas as pd
import numpy as np

# Crear un DataFrame con datos faltantes
data = {
    'Date': pd.date_range(start='2024-01-01', periods=10, freq='D'),
    'Precio': [100, np.nan, np.nan, 105, np.nan, 110, 115, np.nan, 120, 125]
}
df = pd.DataFrame(data).set_index('Date')

# Mostrar datos originales
print("Datos originales:")
print(df)

# Interpolación lineal
df.interpolate(method='linear', inplace=True)

# Mostrar datos interpolados
print("\nDatos interpolados:")
print(df)

# Detección y Eliminación de Duplicados
# Identificar filas duplicadas
duplicados = df[df.duplicated()]
print(duplicados)

# Eliminar Duplicados
df_sin_duplicados = df.drop_duplicates()

# Corrección de Errores en Datos
# Identificar valores fuera de un rango específico
valores_fuera_rango = df[(df['Precio'] < 0) | (df['Precio'] > 1000)]
print(valores_fuera_rango)

# Corrección Manual de Errores:
# Reemplazar un valor específico
df.at[5, 'Precio'] = 150  # Reemplaza el valor en la fila 5, columna 'Precio'

'''3.2.2'''
# Normalización de Datos con Escalado Min-Max
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import yfinance as yf

# Descargar del futuro del Nasdaq en Yahoo Finance
df= yf.download('NQ=F', start='2020-01-01', end='2021-01-01')

scaler = MinMaxScaler()

# Normalizar la columna 'Close'
df['Precio_Normalizado'] = scaler.fit_transform(df[['Close']])
print(df[['Close', 'Precio_Normalizado']].head())

# Estandarización de Datos
from sklearn.preprocessing import StandardScaler

# Crear el escalador estándar
scaler = StandardScaler()

# Estandarizar la columna 'Precio'
df['Precio_Estandarizado'] = scaler.fit_transform(df[['Close']])
print(df[['Close', 'Precio_Estandarizado']].head())

## Transformaciones Adicionales
# Transformación Logarítmica:
import numpy as np

# Aplicar la transformación logarítmica
df['Precio_Log'] = np.log(df['Close'] + 1)  # +1 para evitar log(0)

# Transformación de Potencia:
from scipy import stats

# Aplicar la transformación de Box-Cox
df['Precio_BoxCox'], _ = stats.boxcox(df['Close'] + 1)

## Aplicación a Series Temporales
# Normalización de series temporales usando ventanas deslizantes
window_size = 20
df['Precio_Normalizado_Ventana'] = df['Close'].rolling(window=window_size).apply(
    lambda x: (x[-1] - x.min()) / (x.max() - x.min()) if (x.max() - x.min()) > 0 else 0)

'''3.2.3'''
## Identificación de Outliers

# Método del Rango Intercuartil (IQR):
# calcular el rango intercuartil
Q1 = df['Close'].quantile(0.25)
Q3 = df['Close'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df[(df['Close'] < limite_inferior) | (df['Close'] > limite_superior)]
print(outliers)

# Z-Score (Puntuación Z):
from scipy import stats
import numpy as np

# Calcular el Z-Score para cada valor
df['Z_Score'] = np.abs(stats.zscore(df['Close']))

# Definir un umbral para identificar outliers (por ejemplo, Z > 3)
outliers_z = df[df['Z_Score'] > 3]
print(outliers_z)

# Visualización para Detección de Outliers:
import matplotlib.pyplot as plt

# Crear un boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(df['Close'], vert=False)
plt.title('Boxplot para Detección de Outliers')
plt.xlabel('Close')
plt.show()


## Manejo de Outliers
# Eliminación de Outliers:
# Eliminar outliers utilizando el método IQR
df_sin_outliers = df[(df['Close'] >= limite_inferior) & (df['Close'] <= limite_superior)]
print(df_sin_outliers.head(10))

# Transformación de Outliers:
import numpy as np

# Transformación logarítmica
df['Precio_Log'] = np.log(df['Close'])

# Reemplazo Outliers:
# Reemplazar outliers con la mediana
df.loc[(df['Close'] < limite_inferior) | (df['Close'] > limite_superior), 'Close'] = df['Close'].median()
print(df)


'''3.2.4'''
# Visualización de Datos
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

df= yf.download('AAPL', start='2020-01-01', end='2021-01-01')

# Histograma de la columna 'Close'
plt.figure(figsize=(10, 6))
plt.hist(df['Close'], bins=30, edgecolor='k', alpha=0.7)
plt.title('Distribución del Precio de Cierre')
plt.xlabel('Precio de Cierre')
plt.ylabel('Frecuencia')
plt.show()

# Boxplot
# Boxplot de la columna 'Close'
plt.figure(figsize=(8, 6))
plt.boxplot(df['Close'], vert=False)
plt.title('Boxplot del Precio de Cierre')
plt.xlabel('Precio de Cierre')
plt.show()

# Gráfico de Serie Temporal:
# Gráfico de Serie Temporal
plt.figure(figsize=(12, 6))
plt.plot(df['Close'])
plt.title('Precio de Cierre a lo Largo del Tiempo')
plt.xlabel('precio')
plt.ylabel('Precio de Cierre')
plt.show()

# Análisis Estadístico Descriptivo
# Resumen estadístico
resumen = df.describe()
print(resumen)

# Análisis de Correlación
import seaborn as sns
# Calcular los rendimientos logarítmicos
returns = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].pct_change().dropna()
# Matriz de correlación de los rendimientos
plt.figure(figsize=(10, 6))
matriz_correlacion = returns.corr()
sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Matriz de Correlación de los Rendimientos')
plt.show()

# Identificación de Patrones y Tendencias:
from pandas.plotting import autocorrelation_plot

# Autocorrelación de la serie de tiempo
plt.figure(figsize=(10, 6))
autocorrelation_plot(df['Close'])
plt.title('Autocorrelación del Precio de Cierre')
plt.show()

