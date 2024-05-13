#!/usr/bin/env python3

import socket
import enum

# deve combaciare con l'altro script
PORT = 8008

# NOTA: Mettere l'ip del raspberry
HOST = "127.0.0.1"

stato = None

class Direzione(enum.Enum):
    STOP = 0
    AVANTI = 1
    INDIETRO = 2
    SINISTRA = 3
    DESTRA = 4


try:
    import msvcrt
    import time

    def getch():
        while not msvcrt.kbhit():
            time.sleep(0.01)
        return msvcrt.getch().decode("utf-8")

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


def make_message():
    global stato
    while True:
        c = getch()

        if c == '\x1b' or c == '\x03':
            return None

        if c == 'w' and stato != Direzione.AVANTI:
            print("Avanti")
            stato = Direzione.AVANTI
            return stato.value.to_bytes(1, "big")

        if c == 's' and stato != Direzione.INDIETRO:
            print("Indietro")
            stato = Direzione.INDIETRO
            return stato.value.to_bytes(1, "big")

        if c == 'a' and stato != Direzione.SINISTRA:
            print("Gira a sinistra")
            stato = Direzione.SINISTRA
            return stato.value.to_bytes(1, "big")

        if c == 'd' and stato != Direzione.DESTRA:
            print("Gira a destra")
            stato = Direzione.DESTRA
            return stato.value.to_bytes(1, "big")

        if c.isspace():
            print("Stop")
            stato = Direzione.STOP
            return stato.value.to_bytes(1, "big")

        if c not in ['w','a','s','d']:
            print("Usa wasd o spazio...")

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print("Connesso a", HOST, PORT)

        while True:
            message = make_message()
            if message == None:
                break
            sock.sendall(message)

        print("Uscito dal controller")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Seleziona porta remota", type=int, default=PORT)
    parser.add_argument("--host", help="Seleziona host remoto", type=str, default=HOST)
    args = parser.parse_args()

    PORT = args.port
    HOST= args.host

    client()
