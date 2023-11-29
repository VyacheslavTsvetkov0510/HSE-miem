# библиотеки для постгресс, создания потоков и работы с сокетами
import psycopg2 

import socket 


#коннект база данных
soed1 = psycopg2.connect(baza="Zadanie", user="user1",
    password="12345678pass", host="localhost", port=5432)

cur = soed1.cursor() # подключение к БД
s1 = socket.socket()
s1.bind(('127.0.0.1', 5000))
i=1 # счетчик записей БД
s1.listen(1) # начинаем слушать сокет
soed1 = s1.accept()
cur.execute('CREATE TABLE tableNUM (id INT, num INT)')
baza = cur.fetchall()
cur.execute('CREATE TABLE errortab (id INT, error INT)')
baza = cur.fetchall()
cur.execute('SELECT num FROM tableNUM')
baza = cur.fetchall()
k = 1
while True:
    m = int(soed1.recv(1024))+1
    if m in baza:
        soobsh="Ошибка №1. Попытка записать число повторно".encode("utf-8")
        zapros = """ INSERT INTO errortab (error) VALUES '1' """
        cur.execute()    
    else:
        if (m == baza[k-1]):
            soobsh="Ошибка №2. Введено меньшее число".encode("utf-8")
            zapros = """ INSERT INTO errortab (error) VALUES '0' """
            cur.execute()
        else :
            baza.append(a)
            soobsh = str(a).encode("utf-8")
            zapros = """ INSERT INTO tableNUM (num) VALUES (%s)"""
            cur.execute(zapros, m)
        soed1.commit()
        count = cur.rowcount
    i=i+1
    soed1.send(soobsh)