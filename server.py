import socket
import os

# Настройки сервера
server_ip = '127.0.0.1'  # IP Windows ПК
server_port = 30000

# Создание сокета
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip, server_port))
s.listen(1)

print("Сервер запущен и ожидает подключения...")

conn, addr = s.accept()
print(f"Подключен клиент с адреса {addr}")

while True:
    data = conn.recv(1024).decode()
    
    if data == "exit":
        print("Клиент отключился")
        break
    
    # Проверка, является ли сообщение командой для передачи файла
    if data.startswith("FILE:"):
        # Извлекаем только имя файла
        filename = os.path.basename(data[5:])  
        filesize = conn.recv(1024).decode()  # Получение размера файла
        filesize = int(filesize)

        # Прием файла
        with open(f"received_{filename}", "wb") as f:
            bytes_read = conn.recv(filesize)
            f.write(bytes_read)
        print(f"Файл {filename} получен")
        conn.sendall(f"Файл {filename} получен".encode())
    else:
        print(f"Сообщение от клиента: {data}")
        response = input("Ваш ответ: ")
        conn.sendall(response.encode())

conn.close()
s.close()
