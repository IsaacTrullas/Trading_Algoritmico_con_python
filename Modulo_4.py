'''4.1'''
# Media Móvil Simple (SMA):
# Suponiendo que df es tu DataFrame con la columna 'Close'
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()
print(df[['Close', 'SMA_50', 'SMA_200']])

# Media Móvil Exponencial (EMA):
# Calcular la EMA
df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
print(df[['Close', 'EMA_50', 'EMA_200']])

# MACD
# Calcular el MACD
df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
df['MACD'] = df['EMA_12'] - df['EMA_26']
df['Señal'] = df['MACD'].ewm(span=9, adjust=False).mean()
df['Histograma'] = df['MACD'] - df['Señal']
print(df[['Close', 'MACD', 'Señal', 'Histograma']])

# ADX 
import yfinance as yf
import pandas as pd
import talib as ta

# Descargar del futuro del Nasdaq en Yahoo Finance
df= yf.download('NQ=F', start='2020-01-01', end='2021-01-01')

# Calcular el ADX
df['ADX'] = ta.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
print(df[['Close', 'ADX']])

# RSI 
import talib as ta

# Calcular el RSI
df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
print(df[['Close', 'RSI']])

# Estocástico
# Calcular el Estocástico
df['%K'], df['%D'] = ta.STOCH(df['High'], df['Low'], df['Close'], 
                                fastk_period=14, slowk_period=3, slowk_matype=0, 
                                slowd_period=3, slowd_matype=0)
print(df[['Close', '%K', '%D']])

# Índice de Fuerza de Elder
# Calcular el Índice de Fuerza de Elder
df['Elder_Force'] = (df['Close'] - df['Close'].shift(1)) * df['Volume']
print(df[['Close', 'Volume', 'Elder_Force']])

# Bandas de Bollinger
import pandas as pd

# Calcular las Bandas de Bollinger
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['STD_20'] = df['Close'].rolling(window=20).std()
df['Banda_Superior'] = df['SMA_20'] + (df['STD_20'] * 2)
df['Banda_Inferior'] = df['SMA_20'] - (df['STD_20'] * 2)
print(df[['Close', 'SMA_20', 'Banda_Superior', 'Banda_Inferior']])

# ATR 
# Calcular el ATR
df['TR'] = df['High'] - df['Low']
df['ATR'] = df['TR'].rolling(window=14).mean()
print(df[['Close', 'ATR']])

# CCI 
# Calcular el CCI
df['CCI'] = ta.CCI(df['High'], df['Low'], df['Close'], timeperiod=20)
print(df[['Close', 'CCI']])

# OBV 
# Calcular OBV
df['OBV'] = (df['Close'].diff() > 0).astype(int) * df['Volume'] - (df['Close'].diff() < 0).astype(int) * df['Volume']
df['OBV'] = df['OBV'].cumsum()
print(df[['Close', 'Volume', 'OBV']])

# Volumen Relativo
# Calcular el Volumen Relativo
df['Volumen_Promedio'] = df['Volume'].rolling(window=20).mean()
df['Volumen_Relativo'] = df['Volume'] / df['Volumen_Promedio']
print(df[['Close', 'Volume', 'Volumen_Promedio', 'Volumen_Relativo']])

# Acumulación/Distribución
# Calcular Acumulación/Distribución (A/D)
df['Clv'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
df['A/D'] = (df['Clv'] * df['Volume']).cumsum()
print(df[['Close', 'Volume', 'A/D']])


'''4.2'''

# Regresión Lineal
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Descargar datos del futuro del Nasdaq desde Yahoo Finance
df = yf.download('NQ=F', start='2020-01-01', end='2021-01-01')

# Crear la variable independiente (Días) y la dependiente (Cierre)
df['Dias'] = (df.index - df.index[0]).days  # Crear columna 'Días' a partir de la fecha
X = df[['Dias']]  # Variable independiente
Y = df['Close']   # Variable dependiente (Precio de cierre)

# Dividir los datos en conjunto de entrenamiento y conjunto de prueba
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Crear y ajustar el modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(X_train, Y_train)

# Hacer predicciones sobre el conjunto de prueba
predicciones = modelo.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(Y_test, predicciones)
r2 = r2_score(Y_test, predicciones)

# Mostrar resultados
print(f'Error Cuadrático Medio: {mse}')
print(f'Coeficiente de Determinación (R^2): {r2}')

# Mostrar primeras filas con predicciones
df['Prediccion'] = modelo.predict(X)
print(df[['Close', 'Prediccion']].head())

# Regresión Logística
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score

# Descargar datos del futuro del Nasdaq desde Yahoo Finance
df = yf.download('NQ=F', start='2020-01-01', end='2021-01-01')

# Crear la variable dependiente (1 si el precio sube, 0 si baja)
df['Sube'] = (df['Close'].shift(-1) > df['Close']).astype(int)

# Crear la variable independiente (por ejemplo, el volumen)
X = df[['Volume']]  # Variable independiente
Y = df['Sube']      # Variable dependiente (subida o bajada)

# Dividir los datos en conjunto de entrenamiento y conjunto de prueba
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Crear y ajustar el modelo de regresión logística
modelo = LogisticRegression()
modelo.fit(X_train, Y_train)

# Hacer predicciones sobre el conjunto de prueba
predicciones = modelo.predict(X_test)

# Evaluar el modelo
precision = accuracy_score(Y_test, predicciones)
matriz_confusion = confusion_matrix(Y_test, predicciones)
roc_auc = roc_auc_score(Y_test, modelo.predict_proba(X_test)[:, 1])

# Mostrar resultados
print(f'Precisión: {precision}')
print(f'Matriz de Confusión:\n{matriz_confusion}')
print(f'AUC-ROC: {roc_auc}')
print(df[['Close', 'Sube']].tail())

# ARIMA
import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Descargar los datos
df = yf.download('NQ=F', start='2020-01-01', end='2024-01-01')

# Convertir el índice a columna
df.reset_index(inplace=True)

# Guardar las fechas en una columna separada
dates = df['Date']

# Seleccionar la columna de precios de cierre y numerar el índice de 0 a x
close_prices = df['Close']
close_prices.index = range(len(close_prices))

# Ajustar el modelo ARIMA
model = ARIMA(close_prices, order=(5, 1, 2))
model_fit = model.fit()

# Mostrar el resumen del modelo
print(model_fit.summary())

# Obtener predicciones dentro de la muestra
in_sample_preds = model_fit.predict(start=0, end=len(close_prices)-1)

# Graficar los resultados
plt.figure(figsize=(10, 6))

# Graficar los precios reales y las predicciones dentro de la muestra
plt.plot(dates, close_prices, label='Historical Prices')
plt.plot(dates, in_sample_preds, label='Predictions', linestyle='--', color='green')

plt.title('ARIMA Predictions')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()
plt.show()

# GARCH 
import yfinance as yf
import pandas as pd
from arch import arch_model
import matplotlib.pyplot as plt

# Descargar los datos de Yahoo Finance
df = yf.download('^NDX', start='2020-01-01', end='2024-01-01')

# Calcular los retornos logarítmicos
df['Returns'] = 100 * df['Close'].pct_change()

# Eliminar los valores NaN en la columna de retornos
df = df.dropna()

# Crear el modelo GARCH
model = arch_model(df['Returns'], vol='Garch', p=1, q=1)
garch_fit = model.fit()

# Mostrar el resumen del modelo
print(garch_fit.summary())

# Hacer predicciones de volatilidad in-sample y out-of-sample (OOS)
# Predicciones in-sample
in_sample_forecasts = garch_fit.conditional_volatility

# Predicciones out-of-sample (OOS)
oos_forecasts = garch_fit.forecast(horizon=10)
forecasted_variance = oos_forecasts.variance.iloc[-1]
forecasted_volatility_oos = forecasted_variance ** 0.5  # Volatilidad OOS

# Calcular la volatilidad histórica (rolling std de los retornos)
df['Historical Volatility'] = df['Returns'].rolling(window=30).std()

# Crear un rango de fechas para los próximos 10 días (out-of-sample)
future_dates = pd.date_range(start=df.index[-1], periods=10, freq='B')

# Graficar la volatilidad histórica, in-sample y out-of-sample
plt.figure(figsize=(12, 6))

# Graficar la volatilidad histórica
plt.plot(df.index, df['Historical Volatility'], label='Historical Volatility', color='blue')

# Graficar las predicciones in-sample
plt.plot(df.index, in_sample_forecasts, label='In-Sample Forecasted Volatility', color='orange')

# Graficar las predicciones out-of-sample (OOS)
plt.plot(future_dates, forecasted_volatility_oos, label='Out-of-Sample Forecasted Volatility', linestyle='--', color='red')

# Añadir título y etiquetas
plt.title('Historical vs Forecasted Volatility (GARCH Model)')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.show()

# SARIMA 
import yfinance as yf
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# Descargar los datos del maíz
df = yf.download('ZC=F', start='2015-01-01', end='2024-01-01')

# Convertir el índice a columna
df.reset_index(inplace=True)

# Guardar las fechas y el precio de cierre
dates = df['Date']
close_prices = df['Close']

# Numerar el índice de 0 a x
close_prices.index = range(len(close_prices))

# Ajustar el modelo SARIMA
sarima_model = SARIMAX(close_prices, order=(1,1,1), seasonal_order=(1,1,1,12))
sarima_fit = sarima_model.fit()

# Mostrar el resumen del modelo
print(sarima_fit.summary())

# Obtener predicciones dentro de la muestra
in_sample_preds = sarima_fit.predict(start=0, end=len(close_prices)-1)

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.plot(dates, close_prices, label='Historical Prices')
plt.plot(dates, in_sample_preds, label='Predictions', linestyle='--', color='orange')
plt.title('SARIMA Predictions - Corn Futures')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()


# Random Forests
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Descargar los datos de precios del futuro del Nasdaq
df = yf.download('NQ=F', start='2020-01-01', end='2021-01-01')

# Crear una nueva columna 'Sube' que será nuestro target (1 si sube, 0 si baja)
df['Sube'] = (df['Close'].shift(-1) > df['Close']).astype(int)

# Limpiar datos eliminando NaNs
df.dropna(inplace=True)

# Definir las variables independientes (usaremos solo el precio de cierre para este ejemplo)
X = df[['Close']]
y = df['Sube']

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el Árbol de Decisión
tree_model = DecisionTreeClassifier()
tree_model.fit(X_train, y_train)

# Hacer predicciones
y_pred = tree_model.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del Árbol de Decisión: {accuracy}')
print(classification_report(y_test, y_pred))


#  Random Forest
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report

# Descargar los datos de precios del futuro del Nasdaq
df = yf.download('NQ=F', start='2020-01-01', end='2023-01-01')

# Calcular indicadores técnicos adicionales
df['SMA_10'] = ta.SMA(df['Close'], timeperiod=10)  # Media Móvil Simple de 10 días

# Crear la columna objetivo 'Sube', que indica si el precio sube al día siguiente
df['Sube'] = (df['Close'].shift(-1) > df['Close']).astype(int)

# Limpiar datos eliminando NaNs
df.dropna(inplace=True)

# Definir las variables independientes (indicadores técnicos y precio de cierre)
X = df[['Close', 'SMA_10']]

y = df['Sube']

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definir los hiperparámetros que queremos probar con GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],  # Número de árboles
    'max_depth': [None, 10, 20, 30],  # Profundidad máxima de los árboles
    'min_samples_split': [2, 5, 10],  # Mínimo de muestras para dividir un nodo
    'min_samples_leaf': [1, 2, 4],    # Mínimo de muestras en una hoja
    'bootstrap': [True, False]        # Si utilizar o no el bootstrap
}

# Crear el modelo Random Forest
rf_model = RandomForestClassifier(random_state=42)

# Crear el objeto GridSearchCV
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, 
                        cv=5, n_jobs=-1, verbose=2)

# Ajustar el modelo con los datos de entrenamiento
grid_search.fit(X_train, y_train)

# Imprimir los mejores hiperparámetros encontrados
print(f'Mejores Hiperparámetros: {grid_search.best_params_}')

# Evaluar el modelo con los mejores hiperparámetros
best_rf_model = grid_search.best_estimator_
y_pred = best_rf_model.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del Random Forest después de ajuste: {accuracy}')
print(classification_report(y_test, y_pred))


# LSTM 
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

# Descargar los datos del Nasdaq
df = yf.download('NQ=F', start='2020-01-01', end='2023-01-01')

# Normalizar los datos usando MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
df_scaled = scaler.fit_transform(df[['Close']])

# Preparar los datos para el modelo LSTM
X_train = []
y_train = []
window_size = 60  # Usamos una ventana de 60 días

for i in range(window_size, len(df_scaled)):
    X_train.append(df_scaled[i-window_size:i, 0])
    y_train.append(df_scaled[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Crear el modelo LSTM
model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))  # Capa de salida con una sola unidad (precio predicho)

model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(X_train, y_train, epochs=50, batch_size=32)

# Hacer predicciones sobre nuevos datos
df_test = yf.download('NQ=F', start='2023-01-02', end='2024-01-01')
df_total = pd.concat((df['Close'], df_test['Close']), axis=0)
inputs = df_total[len(df_total) - len(df_test) - window_size:].values
inputs = inputs.reshape(-1,1)
inputs = scaler.transform(inputs)

X_test = []
for i in range(window_size, len(inputs)):
    X_test.append(inputs[i-window_size:i, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Predecir los precios
predicted_price = model.predict(X_test)
predicted_price = scaler.inverse_transform(predicted_price)

# Graficar los resultados
import matplotlib.pyplot as plt

plt.plot(df_test['Close'].values, color='blue', label='Precio Real')
plt.plot(predicted_price, color='red', label='Precio Predicho por LSTM')
plt.title('Predicción de Precio usando LSTM')
plt.xlabel('Fecha')
plt.ylabel('Precio de Cierre')
plt.legend()
plt.show()

# Calcular RMSE
rmse = np.sqrt(mean_squared_error(df_test['Close'].values, predicted_price))

# Calcular MAE
mae = mean_absolute_error(df_test['Close'].values, predicted_price)

# Calcular MAPE
mape = mean_absolute_percentage_error(df_test['Close'].values, predicted_price)

# Generar el resumen del performance
performance_summary = f"""
Evaluación del Modelo LSTM para la Predicción del Nasdaq:

- RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}
- MAE (Error Absoluto Medio): {mae:.2f}
- MAPE (Error Porcentual Absoluto Medio): {mape * 100:.2f}%

"""
print(performance_summary)



# K-Means
import yfinance as yf
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Descargar los datos del índice S&P 500
df = yf.download('^GSPC', start='2015-01-01', end='2023-01-01')

# Calcular características adicionales
df['Price Change'] = df['Close'].pct_change() * 100  #Cambio porcentual diario del precio
df['Volatility'] = df['High'] - df['Low']  #Rango de precios como medida de volatilidad
df['Volume'] = df['Volume']  # Volumen diario

# Limpiar datos eliminando NaNs
df.dropna(inplace=True)

# Seleccionar las características para el clustering
X = df[['Price Change', 'Volatility', 'Volume']]

# Aplicar K-Means con 4 clústeres
kmeans = KMeans(n_clusters=4, random_state=42)
df['Market Regime'] = kmeans.fit_predict(X)

# Visualizar los clústeres identificados por el modelo
sns.scatterplot(x='Price Change', y='Volatility', hue='Market Regime', 
								data=df, palette='Set1')
plt.title('Identificación de Regímenes de Mercado usando K-Means')
plt.xlabel('Cambio Porcentual del Precio')
plt.ylabel('Volatilidad (High - Low)')
plt.show()


# Graficar la línea de cierre y sus regímenes de mercado
plt.figure(figsize=(14, 7))
# Colores para cada clúster
colors = ['#ff0000', '#0000ff', '#00ff00']
plt.plot(df.index, df['Close'], color='black', label='Precio de Cierre')

# Superponer puntos de color según el régimen
for regime in range(3):
    plt.scatter(df.index[df['Market Regime'] == regime], 
						    df['Close'][df['Market Regime'] == regime],
                color=colors[regime], label=f'Regimen {regime}', s=10)

plt.title('Precio de Cierre del S&P 500 con Regímenes de Mercado (K-Means)')
plt.xlabel('Fecha')
plt.ylabel('Precio de Cierre')
plt.legend(loc='best')
plt.show()


# DBSCAN 
import yfinance as yf
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Descargar datos de precios del S&P 500
df = yf.download('^GSPC', start='2015-01-01', end='2024-01-01')

# Calcular el cambio porcentual diario
df['Pct_Change'] = df['Close'].pct_change() * 100

# Calcular la volatilidad diaria (High - Low)
df['Volatility'] = df['High'] - df['Low']

# Limpiar datos eliminando NaNs
df.dropna(inplace=True)

# Normalizar los datos (DBSCAN es sensible a las escalas de los datos)
scaler = StandardScaler()
X = scaler.fit_transform(df[['Pct_Change', 'Volatility']])

# Aplicar DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
df['Cluster'] = dbscan.fit_predict(X)

# Graficar los resultados, marcando las anomalías como 'ruido'
plt.figure(figsize=(10, 6))

# Identificar los puntos de ruido (Cluster -1)
noise = df[df['Cluster'] == -1]
clusters = df[df['Cluster'] != -1]

plt.scatter(clusters['Pct_Change'], clusters['Volatility'], c=clusters['Cluster'], cmap='Set1', label='Clustered Points', alpha=0.6)
plt.scatter(noise['Pct_Change'], noise['Volatility'], c='black', label='Noise (Anomalías)', alpha=0.8)

plt.title('Detección de Patrones Anómalos en el S&P 500 usando DBSCAN')
plt.xlabel('Cambio Porcentual Diario (%)')
plt.ylabel('Volatilidad (High - Low)')
plt.legend()
plt.show()


