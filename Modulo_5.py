# Look-Ahead Bias
import yfinance as yf
import pandas as pd

# Descargar datos de un activo financiero
df = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# Supongamos que queremos basar nuestra estrategia en el precio de cierre del día anterior
df['Close_Anterior'] = df['Close'].shift(1)  # Usamos el cierre del día anterior

# Aquí es donde aplicaríamos la lógica de nuestra estrategia
# df['Signal'] sería una columna con las señales de compra o venta

# Overfitting
import yfinance as yf
import pandas as pd
import numpy as np

# Descargar datos históricos del futuro del Nasdaq
df = yf.download('NQ=F', start='2015-01-01', end='2024-01-01')

# Crear una columna 'Returns' para los rendimientos diarios
df['Returns'] = df['Close'].pct_change()

# Eliminar los valores NaN que pueden surgir al calcular los rendimientos
df.dropna(inplace=True)

# Dividir los datos en tres conjuntos: Desarrollo, Test y Validación
# Aquí vamos a dividir el conjunto de datos en 60% Desarrollo, 20% Test y 20% Validación
n = len(df)
train_size = int(n * 0.6)
test_size = int(n * 0.2)
validation_size = n - train_size - test_size

# Conjunto de Desarrollo
df_train = df.iloc[:train_size]

# Conjunto de Test (fuera de muestra)
df_test = df.iloc[train_size:train_size + test_size]

# Conjunto de Validación (para validación final)
df_validation = df.iloc[train_size + test_size:]

# Mostramos el tamaño de cada conjunto de datos
print(f"Tamaño del conjunto de Desarrollo: {len(df_train)}")
print(f"Tamaño del conjunto de Test: {len(df_test)}")
print(f"Tamaño del conjunto de Validación: {len(df_validation)}")

