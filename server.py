import socket
import threading

HOST = '0.0.0.0'  # Принимает подключения со всех IP
PORT = 12345      # Порт сервера

clients = []

def handle_client(conn, addr):
    try:
        nick = conn.recv(1024).decode()
        print(f"[+] {nick} подключился с {addr}")
        clients.append((conn, nick))
        while True:
            data = conn.recv(1024)
            if not data:
                break
    except Exception as e:
        print(f"[Ошибка клиента {addr}]:", e)
    finally:
        print(f"[-] {addr} отключился")
        conn.close()
        clients.remove((conn, nick))


def start_server():
    print(f"[*] Запуск сервера на {HOST}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен")
    finally:
        s.close()


if __name__ == "__main__":
    start_server()
