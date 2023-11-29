
import socket
from threading import Thread #для одновременной отправки и приема сообщений нам нужно создать два потока данных, прием и передачу

# новое подключение
mySocket = socket.socket()
mySocket.connect("127.0.0.1", 5000)


# функция отправки 
def x():
    while True:
        qwe = input("Запрос к БД")
        mySocket.x(qwe.encode("utf-8"))
        
#функция приема
def y():
    while True:
        ans = mySocket.recv(1024)
        print("Число успешно отправлено! Ответ сервера = ")
        print(ans.decode("utf-8"))

# создаем два канала - прослушка и отправка переменных
tread1 = Thread(target=x)
tread2 = Thread(target=y)

tread1.start()
tread2.start()