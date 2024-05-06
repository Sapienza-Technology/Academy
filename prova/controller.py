#!/usr/bin/env python3

import socket
import enum

# deve combaciare con l'altro script
PORT = 8008

# NOTA: Mettere l'ip del raspberry
HOST = "127.0.0.1"

try:
    import msvcrt
    def getch():
        return msvcrt.getch()

except ImportError:
    import sys, tty, termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class Direzione(enum.Enum):
    STOP = 0
    AVANTI = 1
    INDIETRO = 2
    SINISTRA = 3
    DESTRA = 4

stato = None

def make_message():
    global stato
    while True:
        c = getch()

        if c == '\x1b' or c == '\x03':
            return None

        if c == 'w' and stato != Direzione.AVANTI:
            print("Avanti")
            stato = Direzione.AVANTI
            return stato.value.to_bytes()

        if c == 's' and stato != Direzione.INDIETRO:
            print("Indietro")
            stato = Direzione.INDIETRO
            return stato.value.to_bytes()

        if c == 'a' and stato != Direzione.SINISTRA:
            print("Gira a sinistra")
            stato = Direzione.SINISTRA
            return stato.value.to_bytes()

        if c == 'd' and stato != Direzione.DESTRA:
            print("Gira a destra")
            stato = Direzione.DESTRA
            return stato.value.to_bytes()

        if c.isspace():
            print("Stop")
            stato = Direzione.STOP
            return stato.value.to_bytes()

        if c not in ['w','a','s','d']:
            print("Usa wasd...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    print("Connesso", HOST, PORT)

    while True:
        message = make_message()
        if message == None:
            break
        sock.sendall(message)

    print("Uscito dal controller")
