#!/usr/bin/env python3

import socket
import enum
import gpiozero

# deve combaciare con l'altro script
PORT = 8008

HOST = "0.0.0.0"

class Direzione(enum.Enum):
    STOP = 0
    AVANTI = 1
    INDIETRO = 2
    SINISTRA = 3
    DESTRA = 4

# Interfaccia motori
# TODO: PWM

# Mettere i pin giusti!
front_left = gpiozero.Motor(21, 20, pwm=False)
back_left = gpiozero.Motor(5, 6, pwm=False)
front_right = gpiozero.Motor(26, 16, pwm=False)
back_right = gpiozero.Motor(17, 27, pwm=False)

# Gestisci i messaggi del controller
def handle_client(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            return

        stato = Direzione(int.from_bytes(data))
        print("Ricevuta direzione", stato)

        if stato == Direzione.STOP:
            front_left.stop()
            back_left.stop()
            front_right.stop()
            back_right.stop()

        elif stato == Direzione.AVANTI:
            front_left.forward()
            back_left.forward()
            front_right.forward()
            back_right.forward()

        elif stato == Direzione.INDIETRO:
            front_left.backward()
            back_left.backward()
            front_right.backward()
            back_right.backward()

        elif stato == Direzione.SINISTRA:
            front_left.backward()
            back_left.backward()
            front_right.forward()
            back_right.forward()

        elif stato == Direzione.DESTRA:
            front_left.forward()
            back_left.forward()
            front_right.backward()
            back_right.backward()

        # TODO: Rimanda indietro stato del rover
        sock.sendall(data)

# Connessione remote tramite socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    print("Listening on port", PORT)

    while True:
        try:
            conn, addr = sock.accept()
            print("Connesso", addr)
            handle_client(conn)
            print("Disconnesso", addr)
        except ConnectionResetError:
            print("Disconnessione erronea")

