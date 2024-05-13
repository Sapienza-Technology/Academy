#!/usr/bin/env python3

import socket
import enum

# deve combaciare con l'altro script
PORT = 8008
HOST = "0.0.0.0"

front_left = None
back_left = None
front_right = None
back_right = None

class Direzione(enum.Enum):
    STOP = 0
    AVANTI = 1
    INDIETRO = 2
    SINISTRA = 3
    DESTRA = 4

# Interfaccia motori
# TODO: PWM
def handle_motor(stato):
    print("Nuovo stato", stato)

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

# Gestisci i messaggi del controller
def handle_client(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            return

        print("Ricevuto messaggio", data)
        stato = Direzione(int.from_bytes(data, "big"))

        handle_motor(stato)

        # TODO: Rimanda indietro stato del rover
        sock.sendall(data)

# Connessione remote tramite socket
def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print("Listening on port", PORT)

        while True:
            # Stoppa se si disconnette il client
            handle_motor(Direzione.STOP)

            try:
                conn, addr = sock.accept()
                print("Connesso", addr)
                handle_client(conn)
                print("Disconnesso", addr)
            except ConnectionResetError:
                print("Disconnessione erronea")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--nogpio", help="Disabilita gpiozero", action="store_true")
    parser.add_argument("--port", help="Seleziona porta specifica", type=int, default=PORT)
    args = parser.parse_args()

    PORT = args.port

    if not args.nogpio:
        import gpiozero
        # Mettere i pin giusti!
        front_left = gpiozero.Motor(21, 20, pwm=False)
        back_left = gpiozero.Motor(5, 6, pwm=False)
        front_right = gpiozero.Motor(26, 16, pwm=False)
        back_right = gpiozero.Motor(17, 27, pwm=False)
    else:
        globals()["gpiozero"] = None
        globals()["handle_motor"] = lambda stato: print("Nuovo stato", stato)
        print("GPIO disabilitato")

    server()
