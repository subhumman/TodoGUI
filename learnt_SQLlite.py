import tkinter as tk
from BDclasses import DBmanager, Win

# пандас - это библиотека для работы с данными и их типами(также она позволяет менять расширения и формат файлов)

def main():
    # Создаем менеджер базы данных
    db = DBmanager("TodoList.db")
    
    # Создаем и показываем окно
    window = Win(db, (800, 600), "#FFFFFF")
    window.show()

    return 1

if __name__ == "__main__":
    main()
