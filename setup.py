import sys
from cx_Freeze import setup, Executable
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


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
icon = "icon.ico"


# if sys.platform == "win32":
#    base = "Win32GUI"

setup(name="TraderBot",
      version="0.1",
      description="Aplicação desenvolvida por Felipe de Souza Silva, RA: 106312, para defesa de projeto de TCC da faculdade FHO|Uniararas",
      options={"build_exe": build_exe_options},
      executables=[Executable("app.py", base=base, icon=icon)])
