#!/usr/bin/env python3

from .ansi_colors import *
from time import strftime

# Defining warning messages
def warning(message):
    print("")
    print(f"{yellow}[!]{reset} {message}")

# Defining success messages
def success(message):
    print("")
    print(f"{green}[+]{reset} {message}")

# Defining info messages
def info(message):
    print("")
    print(f"{blue}[i]{reset} {message}")

# Defining error messages
def error(message):
    print("")
    print(f"{red}[-]{reset} {message}")
    exit(1)

# Defining info messages
def alert_time(message):
    print("")
    now = strftime("%d/%m/%Y - %H:%M:%S")
    print(f"[{blue}{now}{reset}]{reset}{reset} {message}")

# Defining info messages
def alert_success(message):
    print("")
    now = strftime("%d/%m/%Y - %H:%M:%S")
    print(f"[{blue}{now}{reset}]{reset}{reset}{green}{reset} {message}")