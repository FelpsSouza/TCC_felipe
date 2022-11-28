import time
import config as cfg
import websocket
import json
import talib
from binance.client import Client
from binance.enums import *
from colorama import Style, Fore
import pandas as pd
from art import *
from playsound import playsound
import csv
from numpy import genfromtxt
import openpyxl
from datetime import datetime
from pytz import timezone
#==============================================================================#

SOCKET = cfg.WsLink
client = Client(cfg.api_key, cfg.api_secret)
closes = []
in_position = False
compra = 0
venda = 0
stopReference = 0
candles = client.get_klines(
    symbol=cfg.TRADE_SYMBOL1, interval=cfg.INTERVAL_TIME)

#==============================================================================#


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    global compra, venda
    try:
        order = client.create_order(
            symbol=symbol, side=side, type=order_type, quantity=quantity)

        print("Enviando ordem: ")
        Timestamp = order['transactTime']
        tempo = pd.to_datetime(Timestamp, unit='ms')
        orderHour = tempo.strftime("%H:%M:%S")

        print(f"Moeda: {order['symbol']}")
        print(f"Tempo: [{orderHour} (UTC)]")
        print(f"Lado da operacao {order['side']}")
        print(f"Tipo de operacao: {order['type']}")
        print(f"Quantidade da criptoMoeda: {order['executedQty']}")
        print(f"Quantidade da moeda: {order['cummulativeQuoteQty']}\n")
        playsound('Sounds/Order.wav')

        if side == SIDE_SELL:
            venda = float(order['cummulativeQuoteQty'])
        if side == SIDE_BUY:
            compra = float(order['cummulativeQuoteQty'])

        if float(compra) > 0 and float(venda) > 0:

            if(compra - venda > 0):
                print(f"Compra: {compra}")
                print(f"Venda: {venda}")
                montante = compra - venda
                print(f"Perda Total = {round(montante,2)}\n")
                playsound('Sounds/Fail.wav')
                compra = 0
                venda = 0

            elif(compra - venda > 0):
                print(f"Compra: {compra}")
                print(f"Venda: {venda}")
                montante = venda - compra
                print(f"Lucro Total = {round(montante,2)}\n")
                playsound('Sounds/Sucess.wav')
                compra = 0
                venda = 0

            else:
                print(f"Compra: {compra}")
                print(f"Venda: {venda}")
                playsound('Sounds/Draw.wav')
                print("Sem perca, sem ganho..\n")
                compra = 0
                venda = 0

    except Exception as error:
        print(Fore.RED)
        print(f"Uma falha foi detectada - {error}")
        print(Style.RESET_ALL)
        playsound('Sounds/Error.wav')

        # inserir metodo que grave erro em um file
        # EXEMPLO:
        # [25/05/2022 - 14:35 - erro de conexão]

        wb = openpyxl.load_workbook('Data/Error_Log.xlsx')
        err_page = wb['Errors']
        err_page.append(['actual_Date', 'actual_Hour', f'{error}'])

        return False

        # 'Connection aborted.', RemoteDisconnected('Remote end closed connection without response')

    return True
#===========================================================================================#


def on_open(ws):
    playsound('Sounds/Start.wav')
    money = cfg.moneyBalance['free']
    print(Fore.GREEN)
    tprint("Robo Trader")
    print(Style.RESET_ALL)
    print(
        f"Usuario: [{cfg.UserName}] | Moeda: [{cfg.TRADE_SYMBOL1}] | Saldo: [{cfg.moneyBalance['asset']} - {round(float(money),2)}] | Tempo: [{cfg.KANDLE_TIME}]\n\n")


def on_close(ws):
    print('Conexão Fechada')


def on_message(ws, message):
    global closes, in_position, stopReference

    csvfile = open('KlineFiles/historicalKline_1.csv', 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    candlestick = client.get_historical_klines(
        cfg.TRADE_SYMBOL1, cfg.INTERVAL_TIME)

    for candlestick in candlestick:
        candlestick[0] = candlestick[0] / 1000
        candlestick_writer.writerow(candlestick)

        closes.append(candlestick[4])

    csvfile.close()

    my_data = genfromtxt('KlineFiles/historicalKline_1.csv', delimiter=',')

    hClose = my_data[:, 4]

    upBand, mdBand, lwBand = talib.BBANDS(
        hClose, cfg.BB_PERIOD, cfg.LWBB_MULT, cfg.UPBB_MULT)

    rsi = talib.RSI(hClose, cfg.RSI_PERIOD)

    last_rsi = rsi[-1]

    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    valorAtual = candle['c']
    moeda = candle['s']
    timestamp = candle['t']

    sTimestamp = str(timestamp)
    sTimestamp = sTimestamp[:10]
    tempo = datetime.fromtimestamp(
        int(sTimestamp), tz=timezone("America/Sao_Paulo"))

    print(f"Valor negociado: {cfg.TRADE_QUANTITY1}")
    print("Moeda: " + Fore.BLUE +
          f"{moeda}" + Style.RESET_ALL)
    print(f"Valor da moeda: {valorAtual}\n")
    print(tempo.strftime("Tempo da vela: [%H:%M (BR)]"))
    print(f"RSI atual: {round(last_rsi, 4)}")
    print(f"UpBand: {round(upBand[-1],4)}")
    print(f"LwBand: {round(lwBand[-1],4)}")

    stopWin = float(stopReference) + (float(stopReference) * cfg.STOP_WIN)
    stopLoss = float(stopReference) - (float(stopReference) * cfg.STOP_LOSS)

    if in_position:
        print(Fore.GREEN + "Procurando venda" + Style.RESET_ALL)
        print(f"Stop Reference: {stopReference}")
        print(f"Stop Win: {stopWin}")
        print(f"Stop Loss: {stopLoss}")
    else:
        print(f"Actual Close: {float(close)}")
        print(Fore.RED + "Procurando compra" + Style.RESET_ALL)

    if is_candle_closed:
        print("#"*45)
        print(f"Vela fechada em {round(float(close),4)}")
        print(f"UpBand fechado em {round(float(upBand[-2]),4)}")
        print(f"LwBand fechado em {round(float(lwBand[-2]),4)}")
        print(Fore.YELLOW +
              f"Ultimo fechamento do RSI: {round(float(last_rsi),4)}\n\n" + Style.RESET_ALL)
#===========================================================================================#
        if (last_rsi > cfg.RSI_OVERBOUGHT and float(close) > float(upBand[-2])):
            if in_position:
                print(Fore.MAGENTA + "Sobrecompra! VENDER! VENDER! VENDER!" +
                      Style.RESET_ALL)
                # [Inserir Lógica de VENDA Binance aqui]
                order_succeeded = order(
                    SIDE_SELL, cfg.TRADE_QUANTITY1, cfg.TRADE_SYMBOL1)

                if order_succeeded:
                    in_position = False
                    stopReference = 0

            else:
                print(
                    "Condições respeitadas, mas não temos nada comprado. Nada a ser feito.")

        elif (float(close) > stopWin) or (float(close) < stopLoss):
            if in_position:
                print(Fore.MAGENTA + "Margem de Seguranca" +
                      Style.RESET_ALL)
                # [Inserir Lógica de VENDA Binance aqui]
                order_succeeded = order(
                    SIDE_SELL, cfg.TRADE_QUANTITY1, cfg.TRADE_SYMBOL1)

                if order_succeeded:
                    in_position = False
                    stopReference = 0

        if (last_rsi < cfg.RSI_OVERSOLD and float(close) < float(lwBand[-2])):
            if in_position:
                print(
                    "Condições respeitadas, mas uma compra ja foi feita. Nada foi feito.")

            else:
                print(Fore.GREEN + "SOBRECOMPRA! COMPRAR! COMPRAR! COMPRAR!" +
                      Style.RESET_ALL)
                # [Inserir Lógica de COMPRA Binance aqui]
                order_succeeded = order(
                    SIDE_BUY, cfg.TRADE_QUANTITY1, cfg.TRADE_SYMBOL1)
                if order_succeeded:
                    stopReference = float(close)
                    in_position = True


#===========================================================================================#


ws = websocket.WebSocketApp(SOCKET, on_open=on_open,
                            on_close=on_close, on_message=on_message)

ws.run_forever()