import tkinter as tk
from BDclasses import DBmanager, Win

def main():
    # Создаем менеджер базы данных
    db = DBmanager("TodoList.db")
    
    # Создаем и показываем окно
    window = Win(db, (800, 600), "#F7F9FB")
    window.show()

    return 1

if __name__ == "__main__":
    main()

'''
    # тут происходит подключение к базе данных с таким вот именем
    fstBD = sqlite3.connect('fstBD.db')

    # тут создается курсос для работы с базой данных
    cursor = fstBD.cursor()

    # тут создается таблица с полями users, id(целочисленное поле, первичный ключ), name(текст), age(целое число)
    fstBD.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)')
'''