from binance.client import Client
print("Loading...")

accConfig = "accConfig.txt"
with open(accConfig, 'r') as file:
    data = file.readlines()

    F_UserName = data[0]
    F_apiKey = data[1]
    F_apiSecret = data[2]

api_key = F_apiKey[8:-1]
api_secret = F_apiSecret[11:-1]
UserName = F_UserName[9:-1]

#==========================CONFIGURAÇÕES DA CORRETORA==========================#
opConfig = "opConfig.txt"
with open(opConfig, 'r') as file:
    data = file.readlines()

    tdSymbolTxt1 = data[0]
    tdSymbolTxt2 = data[1]
    tdSymbolTxt3 = data[2]
    tdSymbolTxt4 = data[3]
    tdSymbolTxt5 = data[4]
    kdTimeTxt = data[6]
    tdQtdTxt1 = data[8]
    tdQtdTxt2 = data[9]
    tdQtdTxt3 = data[10]
    tdQtdTxt4 = data[11]
    tdQtdTxt5 = data[12]
    F_RSIPeriod = data[14]
    F_RSIOverbought = data[15]
    F_RSIOversold = data[16]
    F_BBPeriod = data[18]
    F_BBUp = data[19]
    F_BBLw = data[20]
    F_StopLoss = data[22]
    F_StopWin = data[23]

RSI_PERIOD = float(F_RSIPeriod[11:-1])
RSI_OVERBOUGHT = float(F_RSIOverbought[15:-1])
RSI_OVERSOLD = float(F_RSIOversold[13:-1])

BB_PERIOD = float(F_BBPeriod[10:-1])
UPBB_MULT = float(F_BBUp[11:-1])
LWBB_MULT = float(F_BBLw[11:-1])

STOP_LOSS = float(F_StopLoss[10:-1])  # 01% Um porcento
STOP_WIN = float(F_StopWin[9:-1])  # 01.5% Um e meio porcento


TRADE_SYMBOL1 = tdSymbolTxt1[14:-1]  # Moedas a serem negociadas
TRADE_SYMBOL2 = tdSymbolTxt2[14:-1]
TRADE_SYMBOL3 = tdSymbolTxt3[14:-1]
TRADE_SYMBOL4 = tdSymbolTxt4[14:-1]
TRADE_SYMBOL5 = tdSymbolTxt5[14:-1]

KANDLE_TIME = kdTimeTxt[12:-1]

if KANDLE_TIME == '1m':
    INTERVAL_TIME = Client.KLINE_INTERVAL_1MINUTE

elif KANDLE_TIME == '3m':
    INTERVAL_TIME = Client.KLINE_INTERVAL_3MINUTE

elif KANDLE_TIME == '5m':
    INTERVAL_TIME = Client.KLINE_INTERVAL_5MINUTE

elif KANDLE_TIME == '15m':
    INTERVAL_TIME = Client.KLINE_INTERVAL_15MINUTE

elif KANDLE_TIME == '1h':
    INTERVAL_TIME = Client.KLINE_INTERVAL_1HOUR

elif KANDLE_TIME == '4h':
    INTERVAL_TIME = Client.KLINE_INTERVAL_4HOUR

# ==============================================================================#

WsLink = f"wss://stream.binance.com:9443/ws/{TRADE_SYMBOL1.lower()}@kline_{KANDLE_TIME}"
WsLink2 = f"wss://stream.binance.com:9443/ws/{TRADE_SYMBOL2.lower()}@kline_{KANDLE_TIME}"
WsLink3 = f"wss://stream.binance.com:9443/ws/{TRADE_SYMBOL3.lower()}@kline_{KANDLE_TIME}"
WsLink4 = f"wss://stream.binance.com:9443/ws/{TRADE_SYMBOL4.lower()}@kline_{KANDLE_TIME}"
WsLink5 = f"wss://stream.binance.com:9443/ws/{TRADE_SYMBOL5.lower()}@kline_{KANDLE_TIME}"

client = Client(api_key, api_secret)

moneyBalance = client.get_asset_balance(asset='BRL')
m = moneyBalance['free']


# Valor de moeda negociada #Adicionar a Metodologia
TRADE_QUANTITY1 = tdQtdTxt1[16:-1]
TRADE_QUANTITY2 = tdQtdTxt2[16:-1]
TRADE_QUANTITY3 = tdQtdTxt3[16:-1]
TRADE_QUANTITY4 = tdQtdTxt4[16:-1]
TRADE_QUANTITY5 = tdQtdTxt5[16:-1]

# ==============================================================================#
"""generate_History = True

if generate_History:
    import openpyxl
    import pandas as pd

    trades = client.get_my_trades(symbol=f'{TRADE_SYMBOL}')
    wb = openpyxl.Workbook()
    ws = wb.active

    ws.title = f"{TRADE_SYMBOL} History"
    hs_page = wb[f'{TRADE_SYMBOL} History']
    hs_page.append(['Date', 'Hour', 'Symbol', 'Quantity (R$)', 'Cripto Qty'])
    count = 0
    for i in trades:
        time = i['time']
        End = i['symbol']
        qtd = i['quoteQty']
        cptQtd = i['qty']

        Timestamp = time
        tempo = pd.to_datetime(Timestamp, unit='ms')
        orderHour = tempo.strftime("%H:%M:%S")
        orderDate = tempo.strftime("%d/%m/%Y")

        hs_page.append([f'{orderDate}', f'{orderHour}', f'{End}', f'{round(float(qtd),2)}',
                       f'{round(float(cptQtd),3)}'])

        hs_page['G1'] = "Orders Qty"
        hs_page['G2'] = f'{count}'
        count += 1
    wb.save(f'Data/{TRADE_SYMBOL}_History.xlsx')
"""
