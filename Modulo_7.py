'''7.1.1'''
# Iniciar la conexión con MetaTrader5
import MetaTrader5 as mt5

# iniciar conexión en MetaTrader 5
if not mt5.initialize(login=123456, password='password', server='server'):
    print('Error al inicializar MetaTrader5')
    mt5.shutdown()
    print('Error al inicializar MetaTrader5')
    quit()
else:
    print(f'Conexión establecida con MetaTrader5')


'''7.1.2'''
# Monitoreo del Timeframe
import MetaTrader5 as mt5
from datetime import datetime
import time

# iniciar conexión en MetaTrader 5
if not mt5.initialize(login=123456, password='password', server='server'):
    print('Error al inicializar MetaTrader5')
    mt5.shutdown()
    print('Error al inicializar MetaTrader5')
    quit()
else:
    print(f'Conexión establecida con MetaTrader5')

# Función que ejecuta la estrategia de trading
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")
    # Aquí iría la lógica de trading (adquisición de datos, señales, órdenes, etc.)

# Bucle continuo que monitorea la hora
while True:
    # Obtener la hora actual
    current_time = datetime.now()

    # Comprobar si es la hora de ejecución (22:55:00)
    if current_time.hour == 22 and current_time.minute == 55:
        execute_trading_strategy()
        
        # Dormir por un minuto para evitar ejecutar múltiples veces en el mismo minuto
        time.sleep(60)

    # Esperar un segundo antes de volver a comprobar
    time.sleep(60)


# ejemplo, para un timeframe de 1 hora
# Bucle continuo que monitorea la hora
while True:
    current_time = datetime.now()

    # Comprobar si es el cierre de la hora (cuando el minuto sea 00)
    if current_time.minute == 0:
        execute_trading_strategy()
        time.sleep(60)  # Evitar múltiples ejecuciones en el mismo minuto

    time.sleep(1)


'''7.1.3'''
# Función de adquisición de datos
def get_data(ticker, interval, start, end):
    data = mt5.copy_rates_range(ticker, interval, start, end)
    data = pd.DataFrame(data)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)
    return data


# como nos va quedando el bot:
import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd

# iniciar conexión en MetaTrader 5
if not mt5.initialize(login=123456, password='password', server='server'):
    print('Error al inicializar MetaTrader5')
    mt5.shutdown()
    print('Error al inicializar MetaTrader5')
    quit()
else:
    print(f'Conexión establecida con MetaTrader5')
    
# Función para obtener los datos de precios
def get_data(ticker, interval, start, end):
    data = mt5.copy_rates_range(ticker, interval, start, end)
    data = pd.DataFrame(data)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)
    return data

# Función que ejecuta la estrategia de trading
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")

    '''Aquí iría la lógica de trading (adquisición de datos, señales, órdenes, etc.)'''
    
    # Adquirir los datos necesarios
    df = get_data('NDX', mt5.TIMEFRAME_D1, datetime(2024, 1, 1), datetime.now())

# Bucle continuo que monitorea la hora
while True:
    current_time = datetime.now()

    # Comprobar si es la hora de ejecución (22:55:00)
    if current_time.hour == 22 and current_time.minute == 55:
        execute_trading_strategy()
        time.sleep(60)  # Evitar múltiples ejecuciones en el mismo minuto

    time.sleep(1)  # Esperar un segundo antes de volver a comprobar


'''7.1.4'''
# Ejemplo de lógica de decisión basada en medias móviles
def generate_signal(df):
    # Calcular las medias móviles
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    
    # Generar señal
    if df['SMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]:  # Señal de compra
        return 1
    elif df['SMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]:  # Señal de venta
        return -1
    else:
        return 0  # No hacer nada
    


# Integración de la toma de decisiones en el bot
import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd

# iniciar conexión en MetaTrader 5
if not mt5.initialize(login=123456, password='password', server='server'):
    print('Error al inicializar MetaTrader5')
    mt5.shutdown()
    print('Error al inicializar MetaTrader5')
    quit()
else:
    print(f'Conexión establecida con MetaTrader5')

# Función para obtener los datos de precios
def get_data(ticker, interval, start, end):
    data = mt5.copy_rates_range(ticker, interval, start, end)
    data = pd.DataFrame(data)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)
    return data

# Función que genera la señal de compra o venta
def generate_signal(df):
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    
    if df['SMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]:
        return 1  # Señal de compra
    elif df['SMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]:
        return -1  # Señal de venta
    else:
        return 0  # No hacer nada

# Función que ejecuta la estrategia de trading
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")
    
    # Adquirir los datos
    df = get_data('NDX', mt5.TIMEFRAME_D1, datetime(2024, 1, 1), datetime.now())
    
    # Generar la señal
    signal = generate_signal(df)
    
    # Tomar decisiones según la señal generada
    if signal == 1:
        print("Señal de compra generada.")
        # Aquí iría la ejecución de la orden de compra
    elif signal == -1:
        print("Señal de venta generada.")
        # Aquí iría la ejecución de la orden de venta
    else:
        print("No se ha generado ninguna señal.")
        
# Bucle continuo que monitorea la hora
while True:
    current_time = datetime.now()
    
    # Comprobar si es la hora de ejecución (22:55:00)
    if current_time.hour == 22 and current_time.minute == 55:
        execute_trading_strategy()
        time.sleep(60)  # Evitar múltiples ejecuciones en el mismo minuto

    time.sleep(1)  # Esperar un segundo antes de volver a comprobar


'''7.1.5'''
# Ejecución de órdenes en MetaTrader5
# Función para ejecutar una orden de compra o venta
def place_order(symbol, order_type, volume):
    # Definir los detalles de la orden
    if order_type == 'buy':
        order_type_mt5 = mt5.ORDER_TYPE_BUY
    elif order_type == 'sell':
        order_type_mt5 = mt5.ORDER_TYPE_SELL
    else:
        print("Tipo de orden no válido.")
        return False

    # Obtener el precio actual
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Símbolo {symbol} no encontrado.")
        return False

    price = mt5.symbol_info_tick(symbol).ask if order_type == 'buy' else mt5.symbol_info_tick(symbol).bid

    # Crear la orden
    order = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': volume,
        'type': order_type_mt5,
        'price': price,
        'deviation': 10,
        'magic': 123456,
        'comment': 'Trade ejecutado por bot',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    # Enviar la orden
    result = mt5.order_send(order)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Error al ejecutar la orden: {result.retcode}")
        return False

    print(f"Orden {order_type} de {symbol} ejecutada correctamente. Volumen: {volume}, Precio: {price}")
    return True


# También hemos modificado la función execute_trading_strategy():
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")

    # Adquirir los datos
    df = get_data('NDX', mt5.TIMEFRAME_D1, datetime(2024, 1, 1), datetime.now())

    # Generar la señal
    signal = generate_signal(df)

    # Ejecutar órdenes en función de la señal
    if signal == 1:
        print("Señal de compra generada.")
        place_order('NDX', 'buy', 1.0)  # Orden de compra con un volumen de 1 lote
    elif signal == -1:
        print("Señal de venta generada.")
        place_order('NDX', 'sell', 1.0)  # Orden de venta con un volumen de 1 lote
    else:
        print("No se ha generado ninguna señal.")



# Integración en el bot
import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd

# iniciar conexión en MetaTrader 5
if not mt5.initialize(login=123456, password='password', server='server'):
    print('Error al inicializar MetaTrader5')
    mt5.shutdown()
    print('Error al inicializar MetaTrader5')
else:
    print(f'Conexión establecida con MetaTrader5')
    quit()

# Función para obtener los datos de precios
def get_data(ticker, interval, start, end):
    data = mt5.copy_rates_range(ticker, interval, start, end)
    data = pd.DataFrame(data)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)
    return data

# Función que genera la señal de compra o venta
def generate_signal(df):
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    
    if df['SMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]:
        return 1  # Señal de compra
    elif df['SMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]:
        return -1  # Señal de venta
    else:
        return 0  # No hacer nada

# Función para colocar una orden
def place_order(ticker, order_type, volume):
    if order_type == 'buy':
        request = {
            'action': mt5.TRADE_ACTION_DEAL,
            'symbol': ticker,
            'volume': volume,
            'type': mt5.ORDER_TYPE_BUY,
            'price': mt5.symbol_info_tick(ticker).ask,
            'magic': 123456,
            'comment': 'Estrategia de cruce de medias'
        }
    elif order_type == 'sell':
        request = {
            'action': mt5.TRADE_ACTION_DEAL,
            'symbol': ticker,
            'volume': volume,
            'type': mt5.ORDER_TYPE_SELL,
            'price': mt5.symbol_info_tick(ticker).bid,
            'magic': 123456,
            'comment': 'Estrategia de cruce de medias'
        }
    
    result = mt5.order_send(request)
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Error al colocar la orden: ", result.comment)
    else:
        print("Orden colocada con éxito.")

# Función para ejecutar la estrategia
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")

    # Adquirir los datos
    df = get_data('NDX', mt5.TIMEFRAME_D1, datetime(2024, 1, 1), datetime.now())

    # Generar la señal
    signal = generate_signal(df)

    # Ejecutar órdenes en función de la señal
    if signal == 1:
        print("Señal de compra generada.")
        place_order('NDX', 'buy', 1.0)  # Orden de compra con un volumen de 1 lote
    elif signal == -1:
        print("Señal de venta generada.")
        place_order('NDX', 'sell', 1.0)  # Orden de venta con un volumen de 1 lote
    else:
        print("No se ha generado ninguna señal.")
        
# Bucle continuo que monitorea la hora
while True:
    current_time = datetime.now()
    
    # Comprobar si es la hora de ejecución (22:55:00)
    if current_time.hour == 22 and current_time.minute == 55:
        execute_trading_strategy()
        time.sleep(60)  # Evitar múltiples ejecuciones en el mismo minuto

    time.sleep(1)  # Esperar un segundo antes de volver a comprobar



# Ejemplo de Módulo de Alertas por Email usando GMail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Función para enviar alertas por correo
def send_email_alert(subject, body):
    sender_email = "tu_email@gmail.com"
    receiver_email = "destinatario@gmail.com" # Puede ser el mismo que sender_email
    app_password = "tu_app_password"
    
    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Cuerpo del correo
    msg.attach(MIMEText(body, 'plain'))

    # Configuración del servidor SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    
    # Enviar correo
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# Modificar la ejecución de la estrategia para incluir alertas
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")

    # Lógica de la estrategia (adquisición de datos, señales, órdenes, etc.)
    ...
    # Enviar alerta por correo
    send_email_alert("Alerta de Trading", "Se ha ejecutado una operación en el bot.")



# Ejemplo de Módulo de Control de Festivos
import datetime
import time

# Lista manual de festivos adicionales
manual_holidays = [
    "2024-01-01",  # Año Nuevo
    "2024-04-05",  # Viernes Santo
    "2024-12-25",  # Navidad
]

# Función para comprobar si hoy es festivo (fin de semana o festivo manual)
def is_holiday():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Comprobar si hoy es fin de semana (sábado o domingo)
    if datetime.datetime.now().weekday() >= 5:
        print(f"Hoy es fin de semana ({today}), no se ejecutarán operaciones.")
        return True
    
    # Comprobar si hoy es un festivo manual
    if today in manual_holidays:
        print(f"Hoy es festivo manual: {today}")
        return True
    
    return False

# Función para gestionar la operativa del bot en caso de ser festivo
def manage_trading_on_holiday():
    if is_holiday():
        return False  # No operar si es festivo o fin de semana
    return True  # Seguir con la operativa si no es festivo

# Función principal del bot
def execute_trading_strategy():
    if manage_trading_on_holiday():
        print("Ejecutando estrategia de trading...")
        # Aquí iría el resto de la lógica del bot (adquisición de datos, señales, ejecución de órdenes, etc.)

# Bucle continuo para monitorizar y ejecutar la estrategia
while True:
    current_time = datetime.datetime.now()

    # Comprobar si es la hora de ejecución (por ejemplo, 22:55:00)
    if current_time.hour == 22 and current_time.minute == 55:
        execute_trading_strategy()

    # Esperar un minuto antes de volver a comprobar
    time.sleep(60)



'''7.2.1'''
# Ejemplo: Gestión de capital basada en el riesgo por operación
# Función para calcular el tamaño de la posición basado en el riesgo por operación
def calculate_position_size(capital, risk_per_trade, stop_loss_distance, price):
    
    # El riesgo total es el porcentaje del capital que estamos dispuestos a perder
    risk_amount = capital * risk_per_trade
    
    # Calculamos el tamaño de la posición según la distancia al stop-loss
    position_size = risk_amount / stop_loss_distance
    
    # Convertimos el tamaño de la posición a número de unidades (acciones, contratos, etc.)
    units = position_size / price
    
    return units

# Ejemplo
capital = 100000  # Capital total disponible
risk_per_trade = 0.02  # 2% de riesgo por operación
stop_loss_distance = 50  # Distancia al stop-loss en pips
price = 1500  # Precio actual del activo

# Calcular el tamaño de la posición
units = calculate_position_size(capital, risk_per_trade, stop_loss_distance, price)
print(f"Tamaño de la posición: {units:.2f} unidades")


# Implementación en nuestro Bot
import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd

# iniciar conexión en MetaTrader 5
if not mt5.initialize(login=123456, password='password', server='server'):
    print('Error al inicializar MetaTrader5')
    mt5.shutdown()
    print('Error al inicializar MetaTrader5')
else:
    print(f'Conexión establecida con MetaTrader5')
    quit()

# Función para obtener los datos de precios
def get_data(ticker, interval, start, end):
    data = mt5.copy_rates_range(ticker, interval, start, end)
    data = pd.DataFrame(data)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)
    return data

# Función que genera la señal de compra o venta
def generate_signal(df):
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    
    if df['SMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]:
        return 1  # Señal de compra
    elif df['SMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]:
        return -1  # Señal de venta
    else:
        return 0  # No hacer nada

# Función para colocar una orden (compra o venta)
def place_order(ticker, order_type, volume, sl=0, tp=0):
    # Seleccionar el símbolo en MetaTrader 5
    if not mt5.symbol_select(ticker, True):
        print(f"Error al seleccionar el símbolo {ticker}")
        return None

    # Determinar si la orden es de compra o venta
    if order_type == 'buy':
        order_type_mt5 = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(ticker).ask
    elif order_type == 'sell':
        order_type_mt5 = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(ticker).bid
    else:
        print("Tipo de orden no reconocido. Debe ser 'buy' o 'sell'")
        return None

    # Crear la solicitud de orden
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ticker,
        "volume": volume,
        "type": order_type_mt5,
        "price": price,
        "sl": price - sl if order_type == 'buy' else price + sl,  # SL en función del tipo de orden
        "tp": price + tp if order_type == 'buy' else price - tp,  # TP en función del tipo de orden
        "deviation": 20,  # Desviación permitida
        "magic": 123456,  # Número mágico para identificar la operación
        "comment": f"Python Script {order_type.capitalize()}",
        "type_time": mt5.ORDER_TIME_GTC,  # Good till Cancelled
        "type_filling": mt5.ORDER_FILLING_IOC,  # Immediate or Cancel
    }

    # Comprobar la orden antes de enviarla
    check_result = mt5.order_check(request)
    if check_result is None:
        print("Error al comprobar la orden. El resultado es None.")
        return None
    elif check_result.retcode != 0:
        print(f"No se puede enviar la orden. Código de error: {check_result.retcode}")
        return None

    # Enviar la orden
    result = mt5.order_send(request)
    if result is None:
        print("Error al enviar la orden. El resultado es None.")
        return None
    elif result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"No se ha podido colocar la orden. Código de error: {result.retcode}")
        return None
    else:
        print("Orden colocada con éxito.")
        return result

# Función para calcular el tamaño de lote en función del sl y el riesgo
def lot_calc(ticker, sl, risk):
    # Obtener el equity de la cuenta, que incluye las posiciones abiertas
    equity = mt5.account_info().equity
    
    # Obtener la información del símbolo
    symbol_info = mt5.symbol_info(ticker)

    # Calcular la cantidad de riesgo en términos monetarios (basado en el equity)
    risk_amount = equity * risk

    # Obtener el valor de un pip (en USD)
    pip_value = symbol_info.trade_contract_size * symbol_info.point  # El valor de un pip es el tamaño del contrato por cada punto de movimiento

    # Calcular la distancia al stop-loss en pips
    sl_distance_usd = sl * pip_value  # SL en pips convertido a USD
    
    # Comprobar que la distancia al SL no sea cero
    if sl_distance_usd == 0:
        print("Error: La distancia al stop-loss no puede ser cero.")
        return None

    # Calcular el tamaño de la posición basado en la distancia al stop-loss
    position_size = risk_amount / sl_distance_usd

    # Ajustar el tamaño de la posición a los lotes permitidos por el broker
    lot_min = symbol_info.volume_min
    lot_max = symbol_info.volume_max
    lot_step = symbol_info.volume_step

    # Redondear el tamaño de la posición al lote permitido más cercano
    position_size = max(lot_min, min(round(position_size / lot_step) * lot_step, lot_max))

    return position_size

# Función para ejecutar la estrategia
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")

    # Adquirir los datos
    df = get_data('NDX', mt5.TIMEFRAME_D1, datetime(2024, 1, 1), datetime.now())

    # Generar la señal
    signal = generate_signal(df)

    #Puntos para sl y tp
    sl_point = 1000 # en pips!
    tp_point = 2000 # en pips!
    # Riesgo por operación
    risk = 0.02

    # Ejecutar órdenes en función de la señal
    if signal == 1:
        print("Señal de compra generada.")
        place_order('NDX', 'buy', lot_calc('NDX', sl_point, risk), sl_point, tp_point) #Buy
    elif signal == -1:
        print("Señal de venta generada.")
        place_order('NDX', 'sell', lot_calc('NDX', sl_point, risk), sl_point, tp_point) #Sell
    else:
        print("No se ha generado ninguna señal.")
        
# Bucle continuo que monitorea la hora
while True:
    current_time = datetime.now()
    
    # Comprobar si es la hora de ejecución (22:55:00)
    if current_time.hour == 22 and current_time.minute == 55:
        execute_trading_strategy()
        time.sleep(60)  # Evitar múltiples ejecuciones en el mismo minuto

    time.sleep(1)  # Esperar un segundo antes de volver a comprobar



'''7.2.2'''
# Ejemplo: Implementación de Control de Volatilidad con ATR
def adjust_position_based_on_normalized_atr(ticker, sl, risk, lookback=14):
    # Obtener los datos históricos del activo
    df = get_data(ticker, mt5.TIMEFRAME_D1, datetime(2024, 1, 1), datetime.now())
    
    # Calcular el ATR
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))

    true_range = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    atr = true_range.rolling(window=lookback).mean()

    # Calcular el ATR mínimo y máximo de los últimos x días
    atr_min = atr[-lookback:].min()
    atr_max = atr[-lookback:].max()
    
    # Normalizar el ATR actual entre 0 y 1
    current_atr = atr.iloc[-1]
    normalized_atr = (current_atr - atr_min) / (atr_max - atr_min) if atr_max != atr_min else 0.5
    
    # Llamar a la función lot_calc() para calcular el lotaje basado en el SL y el riesgo
    base_lot_size = lot_calc(ticker, sl, risk)

    # Ajustar el lotaje en función del ATR normalizado
    adjusted_lot_size = base_lot_size * (1 - 0.5 * normalized_atr)

    # Ajustar el tamaño de la posición a los lotes permitidos por el broker
    symbol_info = mt5.symbol_info(ticker)
    lot_min = symbol_info.volume_min
    lot_max = symbol_info.volume_max
    lot_step = symbol_info.volume_step

    # Redondear el tamaño de la posición al lote permitido más cercano
    adjusted_lot_size = max(lot_min, min(round(adjusted_lot_size / lot_step) * lot_step, lot_max))

    return adjusted_lot_size


# Función para ejecutar la estrategia
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")

    # Tickers a operar
    ticker = 'NDX'

    # Adquirir los datos
    df = get_data(ticker, mt5.TIMEFRAME_D1, datetime(2024, 1, 1), datetime.now())

    # Generar la señal
    signal = generate_signal(df)

    #Puntos para sl y tp
    sl_point = 1000 # en pips!
    tp_point = 2000 # en pips!
    # Riesgo por operación
    risk = 0.02

    # calculamos el tamaño de la posición
    lot_size = adjust_position_based_on_normalized_atr(ticker, sl_point, risk)

    # Ejecutar órdenes en función de la señal
    if signal == 1:
        print("Señal de compra generada.")
        place_order('NDX', 'buy', lot_size, sl_point, tp_point) #Buy
    elif signal == -1:
        print("Señal de venta generada.")
        place_order('NDX', 'sell', lot_size, sl_point, tp_point) #Sell
    else:
        print("No se ha generado ninguna señal.")



# Ejemplo: Detección de eventos extremos y protección del bot
def detect_extreme_event(df, threshold=5):
    """
    Detecta si el mercado ha experimentado un movimiento extremo (gap) superior al umbral definido.
    threshold: porcentaje de cambio en el precio que consideramos extremo.
    """
    last_close = df['close'].iloc[-1]
    previous_close = df['close'].iloc[-2]

    price_change = abs((last_close - previous_close) / previous_close) * 100

    if price_change > threshold:
        print(f"Movimiento extremo detectado: {price_change:.2f}%")
        return True
    return False



'''7.2.3'''
# Ejemplo: Protección contra Drawdowns
# Función para calcular el drawdown semanal
def calculate_weekly_drawdown(account_balance, peak_balance):
    return (peak_balance - account_balance) / peak_balance

# Función que implementa la protección contra drawdowns semanales
def weekly_drawdown_protection(account_balance, peak_balance, max_weekly_drawdown):
    current_drawdown = calculate_weekly_drawdown(account_balance, peak_balance)
    
    if current_drawdown >= max_weekly_drawdown:
        print(f"Drawdown semanal excede el límite permitido del {max_weekly_drawdown * 100}%. Operaciones detenidas hasta la próxima semana.")
        return False  # Detener el bot por el resto de la semana
    return True  # Continuar operando

# Variables
max_weekly_drawdown = 0.10  # Máximo drawdown semanal permitido (10%)
peak_balance = 100000  # Balance pico de la cuenta
account_balance = 90000  # Balance actual de la cuenta

# Ejemplo de uso
if weekly_drawdown_protection(account_balance, peak_balance, max_weekly_drawdown):
    print("El bot continúa operando.")
else:
    print("El bot se ha detenido debido al drawdown semanal.")



# Reducción del Lotaje Basada en Drawdowns
# Ajustar el tamaño de las posiciones en función del drawdown semanal
def adjust_position_based_on_weekly_drawdown(account_balance, peak_balance, max_weekly_drawdown, base_lot_size):
    current_drawdown = calculate_weekly_drawdown(account_balance, peak_balance)
    
    # Reducir el lotaje en función del drawdown semanal
    if current_drawdown >= max_weekly_drawdown:
        adjusted_lot_size = base_lot_size * (1 - current_drawdown)
    else:
        adjusted_lot_size = base_lot_size
    
    return max(0, adjusted_lot_size)

# Ejemplo de uso
base_lot_size = 1  # Tamaño de lote inicial
adjusted_lot_size = adjust_position_based_on_weekly_drawdown(account_balance, peak_balance, max_weekly_drawdown, base_lot_size)
print(f"Nuevo tamaño de lote ajustado: {adjusted_lot_size:.2f} lotes")



'''7.3.1'''
# DEBUG (10)
logging.debug('El valor de SMA_50 es 14500 y SMA_200 es 14250.')

# INFO (20)
logging.info('Orden de compra ejecutada a 15000 para el par EUR/USD.')

# WARNING (30)
logging.warning('La volatilidad actual es muy alta. Podría ser riesgoso operar.')

# ERROR (40)
logging.error('Error al ejecutar la orden de venta: conexión fallida.')

# CRITICAL (50)
logging.critical('Desconexión completa de MetaTrader5. Bot detenido.')


# Cómo configurar los niveles de logging en tu bot
import logging

# Configurar el sistema de logging con nivel INFO (no incluirá mensajes DEBUG)
logging.basicConfig(filename='bot_trading.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ejemplos de diferentes niveles de logging
logging.debug('Este es un mensaje DEBUG. Solo se verá si el nivel es DEBUG.')
logging.info('Este es un mensaje INFO. Se verá en niveles INFO o superiores.')
logging.warning('Este es un mensaje WARNING. Se verá en niveles WARNING o superiores.')
logging.error('Este es un mensaje ERROR. Se verá en niveles ERROR o superiores.')
logging.critical('Este es un mensaje CRITICAL. Se verá en niveles CRITICAL o superiores.')


# Ejemplo: Log de operaciones con detalles
import logging

# Configurar el sistema de logging con diferentes niveles
logging.basicConfig(filename='bot_trading.log', 
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Función para registrar la ejecución de la estrategia
def log_strategy_execution(signal, lot_size, close_price, sma_50, sma_200):
    if signal == 1:
        logging.info(f'Se ejecuta una orden de compra de {lot_size} lotes a un precio de cierre de {close_price}.')
        logging.debug(f'Valor del SMA_50: {sma_50}, Valor del SMA_200: {sma_200}')
    elif signal == -1:
        logging.info(f'Se ejecuta una orden de venta de {lot_size} lotes a un precio de cierre de {close_price}.')
        logging.debug(f'Valor del SMA_50: {sma_50}, Valor del SMA_200: {sma_200}')
    else:
        logging.info('No se ha generado ninguna señal.')

# Función para registrar errores
def log_error(error_message):
    logging.error(f"Error: {error_message}")

# Función que ejecuta la estrategia de trading y genera logs avanzados
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")

    # Datos de ejemplo para el log
    signal = 1  # 1 para compra, -1 para venta, 0 para no hacer nada
    lot_size = 0.1
    close_price = 15000  # Precio actual del activo
    sma_50 = 14800  # Valor de la media móvil de 50 días
    sma_200 = 14000  # Valor de la media móvil de 200 días

    try:
        # Registrar la ejecución de la estrategia con detalles
        log_strategy_execution(signal, lot_size, close_price, sma_50, sma_200)
    except Exception as e:
        # Registrar cualquier error que ocurra
        log_error(str(e))



# Ejemplo de Rotación de Logs Basada en Tamaño
import logging
from logging.handlers import RotatingFileHandler

# Configuración de la rotación de logs
handler = RotatingFileHandler('bot_trading.log', maxBytes=5*1024*1024, backupCount=5)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[handler])

# Ejemplo de uso del logging
logging.info('Bot iniciado correctamente.')



# Rotación Basada en Tiempo
from logging.handlers import TimedRotatingFileHandler
import logging

# Configurar rotación semanal de logs
handler = TimedRotatingFileHandler('bot_trading.log', when='W0', interval=1, backupCount=5)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[handler])

# Ejemplo de uso del logging
logging.info('Bot iniciado correctamente.')



# Ejemplo básico: Enviar una alerta a Telegram
import requests

# Configuración del bot de Telegram
telegram_token = 'your_telegram_bot_token'
telegram_chat_id = 'your_chat_id'

def send_telegram_alert(message):
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    payload = {
        'chat_id': telegram_chat_id,
        'text': message
    }
    requests.post(url, data=payload)

# Ejemplo de uso
def execute_trading_strategy():
    print("Estrategia ejecutada a las 22:55")

    # Datos de ejemplo
    signal = 1  # 1 para compra, -1 para venta, 0 para no hacer nada
    lot_size = 0.1
    close_price = 15000  # Precio actual del activo

    # Enviar alerta a Telegram
    if signal == 1:
        message = f"Se ha ejecutado una orden de compra de {lot_size} lotes a un precio de cierre de {close_price}."
    elif signal == -1:
        message = f"Se ha ejecutado una orden de venta de {lot_size} lotes a un precio de cierre de {close_price}."
    else:
        message = "No se ha generado ninguna señal."

    send_telegram_alert(message)



'''7.3.2'''
# Ejemplo de Actualización de Logs y Alertas
import logging
from logging.handlers import TimedRotatingFileHandler
import smtplib

# Configurar rotación semanal de logs
handler = TimedRotatingFileHandler('bot_trading.log', when='W0', interval=1, backupCount=5)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[handler])

# Función para actualizar los logs con nuevos eventos
def log_new_strategy_updates(signal, rsi, var, kelly_fraction):
    if signal == 1:
        logging.info(f'Nueva estrategia ejecutada: Compra con RSI={rsi} y VaR={var}. Fracción de Kelly={kelly_fraction:.2f}')
    elif signal == -1:
        logging.info(f'Nueva estrategia ejecutada: Venta con RSI={rsi} y VaR={var}. Fracción de Kelly={kelly_fraction:.2f}')
    else:
        logging.info(f'Sin señal generada, RSI={rsi}, VaR={var}, Kelly={kelly_fraction:.2f}')

# Función para enviar alertas basadas en KPIs
def send_kpi_alert(email, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('tu_email@gmail.com', 'tu_password_app')
        message = f'Subject: {subject}\n\n{message}'
        server.sendmail('tu_email@gmail.com', email, message)
        server.quit()
        logging.info(f'Alerta enviada a {email} con el asunto: {subject}')
    except Exception as e:
        logging.error(f'Error al enviar alerta: {str(e)}')

# Ejemplo de ejecución de la estrategia y envío de alertas
def execute_updated_strategy():
    signal = 1  # Supongamos que es una señal de compra
    rsi = 55.3
    var = 0.02
    kelly_fraction = 0.25
    
    # Registrar los nuevos eventos en el log
    log_new_strategy_updates(signal, rsi, var, kelly_fraction)
    
    # Enviar alerta si se supera un umbral
    if var > 0.015:
        send_kpi_alert('mi_email@gmail.com', 'Alerta: VaR superado', f'El VaR ha alcanzado {var:.2f}, revisa el bot.')



'''7.3.3'''
# Ejemplo de Monitoreo en Tiempo Real con Logs y Gráficos
import MetaTrader5 as mt5
import logging
import pandas as pd
import matplotlib.pyplot as plt

# Configurar el sistema de logging
logging.basicConfig(filename='bot_realtime.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializar conexión a MetaTrader 5
mt5.initialize()

# Variables de rendimiento
balance_inicial = 100000
balances = []
drawdowns = []

# Función para monitorear rendimiento en tiempo real
def monitor_performance(current_balance, peak_balance):
    # Calcular la rentabilidad
    rentabilidad = (current_balance - balance_inicial) / balance_inicial * 100
    balances.append(current_balance)

    # Calcular el drawdown
    drawdown = (peak_balance - current_balance) / peak_balance * 100
    drawdowns.append(drawdown)

    # Registrar la información en los logs
    logging.info(f'Rentabilidad acumulada: {rentabilidad:.2f}%. Drawdown actual: {drawdown:.2f}%.')

    # Visualización del rendimiento y drawdown en tiempo real
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(balances, label='Balance')
    plt.title('Balance en tiempo real')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(drawdowns, label='Drawdown', color='red')
    plt.title('Drawdown en tiempo real')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Ejemplo de simulación de operación
peak_balance = balance_inicial
for i in range(1, 11):  # Simulamos 10 operaciones
    current_balance = balance_inicial + i * 1000 - i * 200  # Supongamos que hay una ganancia neta
    peak_balance = max(peak_balance, current_balance)  # Actualizamos el pico
    monitor_performance(current_balance, peak_balance)



