'''6.1.1'''
# Ejemplo básico de reglas de entrada y salida
import yfinance as yf
import pandas as pd

# Descargar los datos de un activo
df = yf.download('AAPL', start='2021-01-01', end='2024-01-01')

# Calcular medias móviles
df['SMA_10'] = df['Close'].rolling(window=10).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()

# Definir las reglas de entrada y salida
df['Signal'] = 0  # Inicializamos las señales a 0
df['Signal'][df['SMA_10'] > df['SMA_50']] = 1  # Regla de entrada
f['Signal'].diff() # Detectamos cambios en las señales para identificar entradas y salidas

# eliminamos NaNs
df = df.dropna()

# Imprimir las primeras filas
print(df[['Close', 'SMA_10', 'SMA_50', 'Signal', 'Position']])

'''6.1.2'''
# Construcción de Señales de Trading
import yfinance as yf
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt

# Descargar datos históricos del futuro del Nasdaq
df = yf.download('NQ=F', start='2015-01-01', end='2024-01-01')

# Calcular indicadores
df['SMA_50'] = ta.SMA(df['Close'], timeperiod=50)
df['SMA_200'] = ta.SMA(df['Close'], timeperiod=200)
df['RSI'] = ta.RSI(df['Close'], timeperiod=14)

# Definir reglas de entrada y salida
df['Signal'] = 0
df.loc[(df['RSI'] < 30) & (df['SMA_50'] > df['SMA_200']), 'Signal'] = 1  # Compra
df.loc[(df['RSI'] > 70) & (df['SMA_50'] < df['SMA_200']), 'Signal'] = -1  # Venta

# graficar en un grafico de precios los puntos de compra y venta
plt.figure(figsize=(10, 5))
plt.plot(df['Close'], label='Close')
plt.plot(df.loc[df['Signal'] == 1, 'Close'], '^', markersize=10, color='g', lw=0, label='Buy Signal')
plt.plot(df.loc[df['Signal'] == -1, 'Close'], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
plt.title('AAPL Close Price')
plt.legend()
plt.show()


# Indicadores Combinados
df['ATR'] = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
df['Signal'] = 0  # Inicializamos las señales a 0
df.loc[(df['SMA_10'] > df['SMA_50']) & (df['ATR'] < 2), 'Signal'] = 1


# Señales Basadas en Patrones de Velas
df['Doji'] = ((df['Close'] - df['Open']).abs() < (df['High'] - df['Low']) * 0.1).astype(int)
df.loc[(df['Doji'] == 1) & (df['RSI'] < 30), 'Signal'] = 1  # Comprar cuando se forma un Doji en condiciones de sobreventa


# Contratendencia
df['MACD'] = df['EMA_12'] - df['EMA_26']
df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
df['Signal'] = 0  # Inicializamos las señales a 0
df['Signal'][df['MACD'] > df['Signal_Line']] = 1  # Compra cuando MACD > Línea de señal


'''6.2.2'''
# Ejemplo de Backtesting Básico en Python
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Descargar datos históricos
df = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Calcular medias móviles
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()

# Definir reglas de entrada y salida
df['Signal'] = 0
df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1  # Compra 
df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1  # Vende 

# Simular la ejecución de las órdenes
df['Position'] = df['Signal'].shift()  # Simular la ejecución al siguiente día
df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()  # Retornos de la estrategia

# Eliminar NaNs
df.dropna(inplace=True)

# Graficar el rendimiento de la estrategia frente al activo
(df['Strategy_Returns'] + 1).cumprod().plot(label='Strategy', figsize=(10,5))
(df['Close'].pct_change() + 1).cumprod().plot(label='AAPL')
plt.legend()
plt.show()


# Ejemplo con Backtrader
import backtrader as bt
import yfinance as yf

# Descargar datos usando yfinance
data = bt.feeds.PandasData(dataname=yf.download('AAPL', start='2020-01-01', 
																								end='2024-01-01'))

# Crear una clase de estrategia
class SMACross(bt.Strategy):
    def __init__(self):
        self.sma1 = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.sma2 = bt.indicators.SimpleMovingAverage(self.data.close, period=200)

    def next(self):
        if not self.position:  # No tenemos posición abierta
            if self.sma1 > self.sma2:  # Regla de entrada
                self.buy()
        elif self.sma1 < self.sma2:  # Regla de salida
            self.sell()

# Crear el cerebro y añadir estrategia
cerebro = bt.Cerebro()
cerebro.addstrategy(SMACross)

# Añadir datos al cerebro
cerebro.adddata(data)

# Configurar capital inicial
cerebro.broker.setcash(10000)

# Ejecutar el backtest
print(f'Valor inicial: {cerebro.broker.getvalue()}')
cerebro.run()
print(f'Valor final: {cerebro.broker.getvalue()}')

# Graficar resultados
cerebro.plot()

'''6.2.3'''
# rendimiento anualizado
total_return = (df['Strategy_Returns'] + 1).prod() - 1
annualized_return = (1 + total_return) ** (252 / len(df)) - 1  # Ajustado por 252 días de trading anuales
print(f'Rendimiento Total: {total_return:.2%}')
print(f'Rendimiento Anualizado: {annualized_return:.2%}')


# Ratio de Sharpe
risk_free_rate = 0.01  # Supongamos que la tasa libre de riesgo es del 1%
excess_return = df['Strategy_Returns'].mean() - (risk_free_rate / 252)  # Retornos en exceso sobre la tasa libre de riesgo
sharpe_ratio = excess_return / df['Strategy_Returns'].std()
print(f'Ratio de Sharpe: {sharpe_ratio:.2f}')


# Máximo Drawdown
df['Cumulative_Returns'] = (df['Strategy_Returns'] + 1).cumprod()
df['Peak'] = df['Cumulative_Returns'].cummax()
df['Drawdown'] = (df['Cumulative_Returns'] - df['Peak']) / df['Peak']
max_drawdown = df['Drawdown'].min()
print(f'Máximo Drawdown: {max_drawdown:.2%}')


# Ratio de Ganancias/Pérdidas
winning_trades = df[df['Strategy_Returns'] > 0]['Strategy_Returns'].count()
losing_trades = df[df['Strategy_Returns'] <= 0]['Strategy_Returns'].count()
win_loss_ratio = winning_trades / losing_trades if losing_trades != 0 else np.inf
ganancia_media = df[df['Strategy_Returns'] > 0]['Strategy_Returns'].mean()
perdida_media = df[df['Strategy_Returns'] <= 0]['Strategy_Returns'].mean()
print(f'Operaciones Ganadoras: {winning_trades} -- Ganancia Media: {ganancia_media:.2%}')
print(f'Operaciones Perdedoras: {losing_trades} -- Pérdida Media: {perdida_media:.2%}')
print(f'Ratio Ganancias/Pérdidas: {win_loss_ratio:.2f}')


# Visualización de Resultados
import matplotlib.pyplot as plt

# Graficar el Drawdown
plt.figure(figsize=(10, 5))
df['Drawdown'].plot(label='Drawdown')
plt.title('Drawdown de la Estrategia')
plt.ylabel('Porcentaje de Drawdown')
plt.legend()
plt.show()


# Incorporando Costos Operativos: Comisiones y Slippage
# Simular comisiones y slippage (costos fijos y slippage como porcentaje del precio)
commission = 0.001  # 0.1% por transacción
slippage = 0.0005  # 0.05% de slippage por transacción

df['Transaction_Cost'] = df['Signal'].diff().abs() * (commission + slippage)
df['Net_Strategy_Returns'] = df['Strategy_Returns'] - df['Transaction_Cost']


# Ejemplo del Backtest anterior con metricas incorporadas:
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Descargar datos históricos
df = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Calcular medias móviles
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()

# Definir reglas de entrada y salida
df['Signal'] = 0
df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1  # Compra
df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1  # Vende

# Simular la ejecución de las órdenes
df['Position'] = df['Signal'].shift()  # Shift para simular la ejecución al siguiente día

# Definir comisiones y slippage
commission = 0.001  # 0.1% por operación
slippage = 0.0005  # 0.05% de slippage en cada operación

# Calcular los retornos de la estrategia con comisiones y slippage
df['Returns'] = df['Close'].pct_change()  # Retornos diarios del activo
df['Strategy_Returns'] = df['Position'] * df['Returns']

# Aplicar comisiones y slippage
# Nota: Ajusta los valores de comisiones y slippage según el broker.
df['Strategy_Returns'] -= (abs(df['Position'].diff()) * (commission + slippage))  

# Eliminar NaNs
df.dropna(inplace=True)

# Calcular rendimiento total y anualizado
total_return = (df['Strategy_Returns'] + 1).prod() - 1
annualized_return = (1 + total_return) ** (252 / len(df)) - 1  # Ajustado por 252 días de trading anuales
print(f'Rendimiento Total: {total_return:.2%}')
print(f'Rendimiento Anualizado: {annualized_return:.2%}')

# Ratio de Sharpe
risk_free_rate = 0.01  # Supongamos que la tasa libre de riesgo es del 1%
excess_return = df['Strategy_Returns'].mean() - (risk_free_rate / 252)  # Retornos en exceso sobre la tasa libre de riesgo
sharpe_ratio = excess_return / df['Strategy_Returns'].std()
print(f'Ratio de Sharpe: {sharpe_ratio:.2f}')

# Drawdown Máximo
df['Cumulative_Returns'] = (df['Strategy_Returns'] + 1).cumprod()
df['Peak'] = df['Cumulative_Returns'].cummax()
df['Drawdown'] = (df['Cumulative_Returns'] - df['Peak']) / df['Peak']
max_drawdown = df['Drawdown'].min()
print(f'Máximo Drawdown: {max_drawdown:.2%}')

# Ratio de Ganancias/Pérdidas
winning_trades = df[df['Strategy_Returns'] > 0]['Strategy_Returns'].count()
losing_trades = df[df['Strategy_Returns'] <= 0]['Strategy_Returns'].count()
win_loss_ratio = winning_trades / losing_trades if losing_trades != 0 else np.inf
ganancia_media = df[df['Strategy_Returns'] > 0]['Strategy_Returns'].mean()
perdida_media = df[df['Strategy_Returns'] <= 0]['Strategy_Returns'].mean()
print(f'Operaciones Ganadoras: {winning_trades} -- Ganancia Media: {ganancia_media:.2%}')
print(f'Operaciones Perdedoras: {losing_trades} -- Pérdida Media: {perdida_media:.2%}')
print(f'Ratio Ganancias/Pérdidas: {win_loss_ratio:.2f}')

# Graficar el rendimiento de la estrategia frente al activo
fig, ax1 = plt.subplots(figsize=(10, 5))

# Graficar los rendimientos acumulados de la estrategia
ax1.plot(df.index, df['Cumulative_Returns'], label='Strategy', color='blue', lw=2)

# Graficar los rendimientos acumulados del activo directamente usando Close
ax1.plot(df.index, (df['Close'] / df['Close'].iloc[0]), label='Asset', color='green', lw=2)

ax1.set_ylabel('Cumulative Returns')

# Graficar el drawdown coloreado
ax2 = ax1.twinx()
ax2.fill_between(df.index, df['Drawdown'], 0, color='red', alpha=0.3, label='Drawdown')
ax2.set_ylabel('Drawdown')

# Configurar leyendas y títulos
ax1.legend(loc='upper left')
ax2.legend(loc='lower left')
plt.title('Strategy vs Asset Returns with Drawdown (including commissions and slippage)')

# Mostrar el gráfico
plt.show()

'''6.2.4'''
# Cálculo incorrecto de retornos
# Calcular correctamente los retornos diarios
df['Returns'] = df['Close'].pct_change()


# Aplicar las señales de entrada y salida de forma incorrecta
# Simular la ejecución al día siguiente usando shift
df['Position'] = df['Signal'].shift(1)


# Costos de transacción
# Simular comisiones y slippage
commission = 0.001  # 0.1% por transacción
slippage = 0.0005   # 0.05% de slippage
df['Transaction_Cost'] = df['Signal'].diff().abs() * (commission + slippage)
df['Net_Strategy_Returns'] = df['Strategy_Returns'] - df['Transaction_Cost']


# Falta de ajustes corporativos
# Uso de datos ajustados para evitar errores en backtesting
df = yf.download('AAPL', start='2015-01-01', end='2024-01-01', adjusted=True)

'''6.3.1'''
# Ejemplo de ajuste de parámetros en Python
import yfinance as yf
import pandas as pd
import numpy as np

# Descargar datos históricos
df = yf.download('AAPL', start='2015-01-01', end='2024-01-01')

# Definir función para calcular el rendimiento de la estrategia
def backtest_strategy(short_window, long_window):
    df['SMA_short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['Close'].rolling(window=long_window).mean()
    df['Signal'] = np.where(df['SMA_short'] > df['SMA_long'], 1, -1)
    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()
    return (df['Strategy_Returns'] + 1).cumprod()[-1] - 1  # Retorno total

# Definir el rango de parámetros a probar
short_windows = range(10, 100, 10)  # De 10 a 90 días
long_windows = range(50, 200, 10)  # De 50 a 190 días

# Probar todas las combinaciones de parámetros
best_performance = -np.inf
best_params = (None, None)

for short_window in short_windows:
    for long_window in long_windows:
        if short_window >= long_window:
            continue  # Evitar combinaciones donde la media corta sea mayor o igual a la larga
        performance = backtest_strategy(short_window, long_window)
        if performance > best_performance:
            best_performance = performance
            best_params = (short_window, long_window)

print(f"Mejores parámetros: SMA corta={best_params[0]}, SMA larga={best_params[1]}")
print(f"Mejor rendimiento: {best_performance:.2%}")

'''6.3.2'''
# Grid Search
import yfinance as yf
import pandas as pd
from sklearn.model_selection import ParameterGrid
import numpy as np

# Descargar datos históricos
df = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Rango de valores para las medias móviles
param_grid = {
    'SMA_1': [10, 20, 50], 
    'SMA_2': [100, 150, 200]
}

# Función de backtest para cada combinación de parámetros
def backtest_strategy(sma_1, sma_2):
    df['SMA_50'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_200'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
    df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()
    df.dropna(inplace=True)
    
    # Rendimiento total de la estrategia
    return (df['Strategy_Returns'] + 1).prod() - 1

# Iteramos sobre todas las combinaciones posibles en la grid
best_params = None
best_return = -np.inf

for params in ParameterGrid(param_grid):
    sma_1 = params['SMA_1']
    sma_2 = params['SMA_2']
    total_return = backtest_strategy(sma_1, sma_2)
    print(f'Probando SMA_1: {sma_1}, SMA_2: {sma_2} - Rendimiento Total: {total_return:.2%}')
    
    if total_return > best_return:
        best_return = total_return
        best_params = params

print(f'Los mejores parámetros son: {best_params} con un rendimiento total de {best_return:.2%}')



#  Random Search
import yfinance as yf
import pandas as pd
from sklearn.model_selection import ParameterGrid
import numpy as np

# Descargar datos históricos
df = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Definimos los rangos de parámetros
sma_1_range = np.arange(10, 100, 10)
sma_2_range = np.arange(100, 300, 50)

# Función de backtest para cada combinación de parámetros
def backtest_strategy(sma_1, sma_2):
    df['SMA_50'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_200'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
    df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()
    df.dropna(inplace=True)
    
    return (df['Strategy_Returns'] + 1).prod() - 1

# Seleccionamos aleatoriamente combinaciones de parámetros
best_params = None
best_return = -np.inf

for _ in range(5):  # 5 pruebas aleatorias
    sma_1 = np.random.choice(sma_1_range)
    sma_2 = np.random.choice(sma_2_range)
    
    total_return = backtest_strategy(sma_1, sma_2)
    print(f'Probando SMA_1: {sma_1}, SMA_2: {sma_2} - Rendimiento Total: {total_return:.2%}')
    
    if total_return > best_return:
        best_return = total_return
        best_params = {'SMA_1': sma_1, 'SMA_2': sma_2}

print(f'Los mejores parámetros son: {best_params} con un rendimiento total de {best_return:.2%}')


# Algoritmos Genéticos
import yfinance as yf
import pandas as pd
from deap import base, creator, tools, algorithms
import random

# Descargar datos históricos
df_original = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Función de backtest para cada combinación de parámetros
def backtest_strategy(sma_1, sma_2):
    # Asegurarse de que sean enteros
    sma_1 = int(sma_1)
    sma_2 = int(sma_2)
    
    # Hacer una copia del DataFrame original para cada evaluación
    df = df_original.copy()
    
    # Calcular medias móviles
    df['SMA_50'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_200'] = df['Close'].rolling(window=sma_2).mean()
    
    # Definir reglas de entrada y salida
    df['Signal'] = 0
    df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
    df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1
    
    # Simular la ejecución de las órdenes
    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()
    
    # Eliminar NaNs
    df.dropna(inplace=True)
    
    # Rendimiento total de la estrategia
    return (df['Strategy_Returns'] + 1).prod() - 1

# Función de evaluación
def evaluate(individual):
    sma_1, sma_2 = individual
    # Validar que ambos valores sean mayores que 0 y que SMA_1 < SMA_2
    if sma_1 <= 0 or sma_2 <= 0 or sma_1 >= sma_2:
        return -np.inf,  # Penalización por una configuración inválida
    total_return = backtest_strategy(sma_1, sma_2)
    return (total_return,)

# Crear individuo y configuración genética
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Registro de los atributos de las medias móviles como enteros
toolbox.register("attr_sma1", random.randint, 10, 100)
toolbox.register("attr_sma2", random.randint, 100, 300)
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.attr_sma1, toolbox.attr_sma2), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Registro de la función de evaluación
toolbox.register("evaluate", evaluate)

# Operadores genéticos: cruza y mutación ajustados para enteros
toolbox.register("mate", tools.cxUniform, indpb=0.5)  # cxUniform mezcla valores enteros
toolbox.register("mutate", tools.mutUniformInt, low=[10, 100], up=[100, 300], indpb=0.2)  # mutUniformInt para mantener enteros
toolbox.register("select", tools.selTournament, tournsize=3)

# Ejecutar algoritmo genético
population = toolbox.population(n=10)

# Algoritmo evolutivo simple
algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.2, ngen=10, verbose=True)

# Imprimir los mejores resultados
best_individual = tools.selBest(population, k=1)[0]
best_return = evaluate(best_individual)[0]  # Calcular el mejor rendimiento

print(f'Los mejores parámetros son SMA_1: {int(best_individual[0])}, SMA_2: {int(best_individual[1])}')
print(f'El mejor rendimiento total es: {best_return:.2%}')


# Simulated Annealing
import yfinance as yf
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Descargar datos históricos
df_original = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Función de backtest para cada combinación de parámetros
def backtest_strategy(sma_1, sma_2):
    df = df_original.copy()
    df['SMA_50'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_200'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
    df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()

    df.dropna(inplace=True)

    # Rendimiento total de la estrategia
    return (df['Strategy_Returns'] + 1).prod() - 1

# Función de aceptación de Simulated Annealing
def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost > old_cost:
        return 1.0
    else:
        return np.exp((new_cost - old_cost) / temperature)

# Función de Simulated Annealing
def simulated_annealing(initial_sma_1, initial_sma_2, initial_temp, cooling_rate, max_iter):
    current_sma_1 = initial_sma_1
    current_sma_2 = initial_sma_2
    current_cost = backtest_strategy(current_sma_1, current_sma_2)
    best_sma_1, best_sma_2 = current_sma_1, current_sma_2
    best_cost = current_cost
    temp = initial_temp

    for i in range(max_iter):
        # Generar nuevos parámetros vecinos (cercanos a los actuales)
        new_sma_1 = current_sma_1 + random.randint(-5, 5)
        new_sma_2 = current_sma_2 + random.randint(-5, 5)

        # Asegurarse de que los parámetros tengan sentido (evitar valores negativos o cruces imposibles)
        new_sma_1 = max(10, new_sma_1)
        new_sma_2 = max(20, new_sma_2)
        new_sma_2 = max(new_sma_1 + 10, new_sma_2)  # Asegurar que SMA_2 sea mayor que SMA_1

        # Calcular el nuevo costo (rendimiento) con los nuevos parámetros
        new_cost = backtest_strategy(new_sma_1, new_sma_2)

        # Decidir si aceptamos la nueva solución o no
        if acceptance_probability(current_cost, new_cost, temp) > random.random():
            current_sma_1 = new_sma_1
            current_sma_2 = new_sma_2
            current_cost = new_cost

        # Actualizar la mejor solución encontrada
        if new_cost > best_cost:
            best_sma_1, best_sma_2 = new_sma_1, new_sma_2
            best_cost = new_cost

        # Enfriar la temperatura
        temp *= cooling_rate

        print(f'Iteración {i+1}: Mejor SMA_1 = {best_sma_1}, Mejor SMA_2 = {best_sma_2}, Mejor Rendimiento = {best_cost:.2%}')
    
    return best_sma_1, best_sma_2, best_cost

# Parámetros iniciales para Simulated Annealing
initial_sma_1 = 100
initial_sma_2 = 300
initial_temp = 1000
cooling_rate = 0.95
max_iter = 100

# Ejecutar el algoritmo de Simulated Annealing
best_sma_1, best_sma_2, best_return = simulated_annealing(initial_sma_1, initial_sma_2, initial_temp, cooling_rate, max_iter)

print(f'Los mejores parámetros son SMA_1: {best_sma_1}, SMA_2: {best_sma_2} con un rendimiento total de {best_return:.2%}')


# Optimización Basada en Múltiples Métricas

# Ratio de Sharpe
import yfinance as yf
import pandas as pd
import numpy as np


# Descargar datos históricos
df = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

def backtest_strategy(sma_1, sma_2):
    df['SMA_50'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_200'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
    df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()
    df.dropna(inplace=True)

    # Calcular el ratio de Sharpe
    risk_free_rate = 0.01  # 1% tasa libre de riesgo
    excess_return = df['Strategy_Returns'].mean() - (risk_free_rate / 252)
    sharpe_ratio = excess_return / df['Strategy_Returns'].std()
    
    return sharpe_ratio

# Optimización mediante Grid Search
best_params = None
best_sharpe = -np.inf

for sma_1 in range(10, 100, 10):
    for sma_2 in range(100, 300, 50):
        sharpe = backtest_strategy(sma_1, sma_2)
        print(f'Probando SMA_1: {sma_1}, SMA_2: {sma_2} - Ratio de Sharpe: {sharpe:.2f}')
        
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_params = (sma_1, sma_2)

print(f'Los mejores parámetros son: {best_params} con un Ratio de Sharpe de {best_sharpe:.2f}')


# Drawdown Máximo
import yfinance as yf
import pandas as pd
import numpy as np


# Descargar datos históricos
df = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

def backtest_strategy(sma_1, sma_2):
    df['SMA_50'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_200'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
    df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()
    df.dropna(inplace=True)

    # Calcular drawdown máximo
    df['Cumulative_Returns'] = (df['Strategy_Returns'] + 1).cumprod()
    df['Peak'] = df['Cumulative_Returns'].cummax()
    df['Drawdown'] = (df['Cumulative_Returns'] - df['Peak']) / df['Peak']
    max_drawdown = df['Drawdown'].min()
    
    return max_drawdown

# Optimización mediante Grid Search
best_params = None
best_drawdown = np.inf

for sma_1 in range(10, 100, 10):
    for sma_2 in range(100, 300, 50):
        drawdown = backtest_strategy(sma_1, sma_2)
        print(f'Probando SMA_1: {sma_1}, SMA_2: {sma_2} - Máximo Drawdown: {drawdown:.2%}')
        
        if abs(drawdown) < abs(best_drawdown):  # Compara la magnitud del drawdown
            best_drawdown = drawdown
            best_params = (sma_1, sma_2)

print(f'Los mejores parámetros son: {best_params} con un Máximo Drawdown de {best_drawdown:.2%}')


# Ratio de Calmar
import yfinance as yf
import pandas as pd
import numpy as np

# Descargar datos históricos
df = yf.download('NQ=F', start='2000-01-01', end='2024-01-01')

def backtest_strategy(sma_1, sma_2):
    # Cálculo de SMAs
    df['SMA_50'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_200'] = df['Close'].rolling(window=sma_2).mean()

    # Señales de trading
    df['Signal'] = 0
    df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
    df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1

    # Posición basada en la señal
    df['Position'] = df['Signal'].shift()
    
    # Comprobar que se generaron suficientes señales
    num_signals = df['Position'].diff().abs().sum()  # Número de cambios de señal
    if num_signals < 10:  # Ajusta este umbral según lo que consideres relevante
        return np.nan
    
    # Retornos de la estrategia
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()
    df.dropna(inplace=True)  # Eliminar filas con NaN
    
    # Asegurarse de que hay suficientes datos
    if len(df) == 0:
        return np.nan
    
    # Calcular drawdown máximo y rendimiento anualizado
    df['Cumulative_Returns'] = (df['Strategy_Returns'] + 1).cumprod()
    df['Peak'] = df['Cumulative_Returns'].cummax()
    df['Drawdown'] = (df['Cumulative_Returns'] - df['Peak']) / df['Peak']
    
    max_drawdown = df['Drawdown'].min()
    total_return = (df['Strategy_Returns'] + 1).prod() - 1
    annualized_return = (1 + total_return) ** (252 / len(df)) - 1

    # Controlar retornos anómalos
    if total_return > 10:  # Si el retorno acumulado es absurdo
        total_return = 10  # Ajustar a un valor razonable
    
    # Evitar división por cero en el Ratio de Calmar
    if max_drawdown == 0 or np.isnan(max_drawdown):
        return np.nan  # Retornar NaN si no hay drawdown o es cero
    
    calmar_ratio = annualized_return / abs(max_drawdown)

    # Limitar valores desproporcionados de Calmar Ratio
    if calmar_ratio > 10:  # Puedes ajustar este umbral
        calmar_ratio = 10  # Limitar a un máximo razonable

    return calmar_ratio

# Optimización mediante Grid Search
best_params = None
best_calmar = -np.inf

for sma_1 in range(10, 100, 10):
    for sma_2 in range(100, 300, 50):
        calmar_ratio = backtest_strategy(sma_1, sma_2)
        if not np.isnan(calmar_ratio):  # Evitar comparar con NaN
            if calmar_ratio > best_calmar:
                best_calmar = calmar_ratio
                best_params = (sma_1, sma_2)

print(f'Los mejores parámetros son: {best_params} con un Ratio de Calmar de {best_calmar:.2f}')


'''6.4.1'''
# Ejemplo práctico: Separación de datos
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Descargar datos históricos del futuro del Nasdaq
df = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# División de datos en entrenamiento (60%), test (20%) y validación (20%)
train_size = int(len(df) * 0.6)
test_size = int(len(df) * 0.2)

train_data = df[:train_size]
test_data = df[train_size:train_size+test_size]
validation_data = df[train_size+test_size:]

# Verificar las dimensiones de los conjuntos
print("Tamaño del conjunto de Entrenamiento:", train_data.shape)
print("Tamaño del conjunto de Test:", test_data.shape)
print("Tamaño del conjunto de Validación:", validation_data.shape)

# Graficar los diferentes conjuntos de datos
plt.figure(figsize=(10,5))
plt.plot(train_data['Close'], label='Entrenamiento', color='blue')
plt.plot(test_data['Close'], label='Test', color='orange')
plt.plot(validation_data['Close'], label='Validación', color='green')
plt.title('Separación de Datos: Entrenamiento, Test y Validación')
plt.legend()
plt.show()


'''6.4.2'''
# Ejemplo: Evaluación con datos fuera de muestra
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Descargar datos históricos
df_original = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Separar los datos en entrenamiento (80%) y validación (20%)
train_size = int(len(df_original) * 0.8)
train_data = df_original[:train_size]
validation_data = df_original[train_size:]

# Función de backtest para cada combinación de parámetros
def backtest_strategy(data, sma_1, sma_2):
    df = data.copy()
    df['SMA_1'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_2'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_1'] > df['SMA_2'], 'Signal'] = 1
    df.loc[df['SMA_1'] < df['SMA_2'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()

    df.dropna(inplace=True)

    # Retornar el DataFrame con los cálculos
    return df

# Rango de valores para la optimización
sma_1_range = range(10, 50, 5)
sma_2_range = range(100, 300, 25)

# Optimización con Grid Search en el conjunto de entrenamiento
best_params = None
best_return_train = -np.inf

for sma_1 in sma_1_range:
    for sma_2 in sma_2_range:
        df_train_result = backtest_strategy(train_data, sma_1, sma_2)
        total_return_train = (df_train_result['Strategy_Returns'] + 1).prod() - 1
        print(f'Probando SMA_1: {sma_1}, SMA_2: {sma_2} - Rendimiento en Entrenamiento: {total_return_train:.2%}')
        
        if total_return_train > best_return_train:
            best_return_train = total_return_train
            best_params = (sma_1, sma_2)

print(f'\nMejores parámetros en entrenamiento: SMA_1: {best_params[0]}, SMA_2: {best_params[1]} con un rendimiento total de {best_return_train:.2%}')

# Evaluar en el conjunto de validación con los mejores parámetros
df_validation_result = backtest_strategy(validation_data, best_params[0], best_params[1])
best_return_validation = (df_validation_result['Strategy_Returns'] + 1).prod() - 1
print(f'Rendimiento en validación con los mejores parámetros: {best_return_validation:.2%}')

# Calcular rendimientos acumulados de entrenamiento
train_cumulative_returns = np.cumprod(df_train_result['Strategy_Returns'] + 1)

# Calcular rendimientos acumulados de validación, comenzando desde el último valor de entrenamiento
last_train_value = train_cumulative_returns.iloc[-1]
validation_cumulative_returns = np.cumprod(df_validation_result['Strategy_Returns'] + 1) * last_train_value

# Graficar resultados de entrenamiento y validación solapados
plt.figure(figsize=(14, 7))
plt.plot(train_cumulative_returns, label='Entrenamiento', color='blue')
plt.plot(validation_cumulative_returns, label='Validación', color='orange')
plt.title('Rendimiento Acumulado en Entrenamiento vs Validación (solapados)')
plt.xlabel('Fecha')
plt.ylabel('Rendimiento acumulado')
plt.legend()
plt.show()


'''6.4.3'''
# Ejemplo de Walk-Forward Optimization
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Descargar datos históricos
df_original = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Función de backtest para cada combinación de parámetros
def backtest_strategy(data, sma_1, sma_2):
    df = data.copy()
    df['SMA_1'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_2'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_1'] > df['SMA_2'], 'Signal'] = 1
    df.loc[df['SMA_1'] < df['SMA_2'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()

    df.dropna(inplace=True)

    # Retornar el DataFrame con los cálculos
    return df

# Configuración de la optimización walk-forward
train_window = 3 * 252  # 3 años de datos para entrenamiento (252 días de trading por año)
validation_window = 1 * 252  # 1 año de datos para validación
total_window = train_window + validation_window

# Rango de valores para optimización de medias móviles
sma_1_range = range(10, 50, 5)
sma_2_range = range(100, 300, 25)

# Listas para acumular resultados
validation_returns = []
train_returns = []

# Realizar la optimización Walk-Forward
for start in range(0, len(df_original) - total_window, validation_window):
    # Separar los datos en entrenamiento y validación
    train_data = df_original[start:start + train_window]
    validation_data = df_original[start + train_window:start + total_window]

    # Optimización en el conjunto de entrenamiento
    best_params = None
    best_return_train = -np.inf

    for sma_1 in sma_1_range:
        for sma_2 in sma_2_range:
            df_train_result = backtest_strategy(train_data, sma_1, sma_2)
            total_return_train = (df_train_result['Strategy_Returns'] + 1).prod() - 1
            
            if total_return_train > best_return_train:
                best_return_train = total_return_train
                best_params = (sma_1, sma_2)
    
    train_returns.append(best_return_train)

    # Evaluar en el conjunto de validación con los mejores parámetros
    df_validation_result = backtest_strategy(validation_data, best_params[0], best_params[1])
    total_return_validation = (df_validation_result['Strategy_Returns'] + 1).prod() - 1
    validation_returns.append(total_return_validation)

    print(f'Periodo {start // validation_window + 1}: Mejores parámetros en entrenamiento: SMA_1: {best_params[0]}, SMA_2: {best_params[1]}')
    print(f'Rendimiento en entrenamiento: {best_return_train:.2%}, Rendimiento en validación: {total_return_validation:.2%}\n')

# Evaluar el rendimiento total en validación fuera de muestra
print(f'Rendimiento promedio en validación fuera de muestra: {np.mean(validation_returns):.2%}')


'''6.4.4'''
# Ejemplo de Análisis de Sensibilidad
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Descargar datos históricos
df_original = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Función de backtest para la estrategia de medias móviles con cálculo de Sharpe
def backtest_strategy(data, sma_1, sma_2):
    df = data.copy()
    df['SMA_1'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_2'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_1'] > df['SMA_2'], 'Signal'] = 1
    df.loc[df['SMA_1'] < df['SMA_2'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()

    df.dropna(inplace=True)

    # Calcular el rendimiento total
    total_return = (df['Strategy_Returns'] + 1).prod() - 1

    # Calcular el ratio de Sharpe (asumimos rendimiento libre de riesgo = 0)
    avg_return = df['Strategy_Returns'].mean()
    risk = df['Strategy_Returns'].std()
    sharpe_ratio = avg_return / risk if risk != 0 else np.nan

    return total_return, sharpe_ratio

# Parámetros base optimizados
base_sma_1 = 50
base_sma_2 = 200

# Rango de variación para el análisis de sensibilidad
sma_1_range = [45, 50, 55]
sma_2_range = [195, 200, 205]

# Realizar el análisis de sensibilidad
sens_results = []

for sma_1 in sma_1_range:
    for sma_2 in sma_2_range:
        total_return, sharpe_ratio = backtest_strategy(df_original, sma_1, sma_2)
        sens_results.append((sma_1, sma_2, total_return, sharpe_ratio))
        print(f'SMA_1: {sma_1}, SMA_2: {sma_2} - Rendimiento Total: {total_return:.2%}, Sharpe Ratio: {sharpe_ratio:.2f}')

# Ordenar los resultados por rendimiento
sens_results.sort(key=lambda x: x[2], reverse=True)

# Calcular la desviación estándar de los Sharpe Ratios
sharpe_ratios = [res[3] for res in sens_results if not np.isnan(res[3])]
sharpe_std = np.std(sharpe_ratios)

# Mostrar los resultados
print("\nResultados del análisis de sensibilidad (ordenados por rendimiento):")
for res in sens_results:
    print(f'SMA_1: {res[0]}, SMA_2: {res[1]} - Rendimiento Total: {res[2]:.2%}, Sharpe Ratio: {res[3]:.2f}')

print(f"\nDesviación estándar de los Sharpe Ratios: {sharpe_std:.4f}")

# Calcular el Sharpe Ratio original
_, sharpe_original = backtest_strategy(df_original, base_sma_1, base_sma_2)

# Graficar la curva de densidad del Sharpe Ratio
kde = gaussian_kde(sharpe_ratios)
x_range = np.linspace(min(sharpe_ratios), max(sharpe_ratios), 100)
plt.plot(x_range, kde(x_range), label='Curva de Distribución de Sharpe Ratios', color='b')

# Añadir la línea del Sharpe Ratio original
plt.axvline(x=sharpe_original, color='r', linestyle='--', label=f'Sharpe Original ({sharpe_original:.2f})')

plt.title('Distribución de Sharpe Ratios vs Sharpe Original')
plt.xlabel('Sharpe Ratio')
plt.ylabel('Densidad')
plt.legend()
plt.show()


# Evaluación de la Robustez
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Descargar datos históricos para el análisis de sensibilidad y robustez
df_original = yf.download('NQ=F', start='2010-01-01', end='2024-01-01')

# Función de backtest para la estrategia de medias móviles con cálculo de Sharpe y retorno total
def backtest_strategy(data, sma_1, sma_2):
    df = data.copy()
    df['SMA_1'] = df['Close'].rolling(window=sma_1).mean()
    df['SMA_2'] = df['Close'].rolling(window=sma_2).mean()

    df['Signal'] = 0
    df.loc[df['SMA_1'] > df['SMA_2'], 'Signal'] = 1
    df.loc[df['SMA_1'] < df['SMA_2'], 'Signal'] = -1

    df['Position'] = df['Signal'].shift()
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()

    df.dropna(inplace=True)

    # Calcular el rendimiento total
    total_return = (df['Strategy_Returns'] + 1).prod() - 1

    # Calcular el ratio de Sharpe (asumimos rendimiento libre de riesgo = 0)
    avg_return = df['Strategy_Returns'].mean()
    risk = df['Strategy_Returns'].std()
    sharpe_ratio = avg_return / risk if risk != 0 else np.nan

    return total_return, sharpe_ratio

# Parámetros base optimizados
base_sma_1 = 50
base_sma_2 = 200

# Definir diferentes periodos para pruebas de robustez
periods = [
    ('2010-01-01', '2013-01-01'),
    ('2013-01-01', '2016-01-01'),
    ('2016-01-01', '2019-01-01'),
    ('2019-01-01', '2024-01-01')
]

# Evaluar la estrategia en diferentes periodos
print("Evaluación de Robustez - Resultados en Diferentes Periodos de Tiempo")
for start, end in periods:
    df_period = yf.download('NQ=F', start=start, end=end)
    total_return, sharpe_ratio = backtest_strategy(df_period, base_sma_1, base_sma_2)
    print(f'Periodo {start} a {end} - Rendimiento Total: {total_return:.2%}, Sharpe Ratio: {sharpe_ratio:.2f}')

# Visualizar resultados para robustez en cada periodo (rendimiento acumulado)
plt.figure(figsize=(12, 6))

for start, end in periods:
    df_period = yf.download('NQ=F', start=start, end=end)
    df_period_result = backtest_strategy(df_period, base_sma_1, base_sma_2)
    cumulative_returns = np.cumprod(df_period['Close'].pct_change() + 1)
    plt.plot(cumulative_returns, label=f'Periodo {start} a {end}')

plt.title('Rendimiento Acumulado en Diferentes Periodos de Tiempo (Prueba de Robustez)')
plt.xlabel('Fecha')
plt.ylabel('Rendimiento acumulado')
plt.legend()
plt.show()


