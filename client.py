import socket
import os

# Настройки клиента
server_ip = '127.0.0.1'  # IP Kali Linux ПК
server_port = 30000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, server_port))

print("Подключение установлено.")

def send_file(filename):
    filesize = os.path.getsize(filename)

    # Отправка команды и имени файла
    s.sendall(f"FILE:{filename}".encode())

    # Отправка размера файла
    s.sendall(str(filesize).encode())

    # Чтение и отправка файла
    with open(filename, "rb") as f:
        bytes_read = f.read(filesize)
        s.sendall(bytes_read)
    print(f"Файл {filename} отправлен")

while True:
    message = input("Введите сообщение или путь к файлу: ")
    
    if message == "exit":
        s.sendall(message.encode())
        print("Отключение...")
        break
    elif os.path.isfile(message):
        send_file(message)
    else:
        s.sendall(message.encode())
        response = s.recv(1024).decode()
        print(f"Ответ от сервера: {response}")

s.close()
