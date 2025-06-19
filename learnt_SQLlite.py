import tkinter as tk
from BDclasses import DBmanager, Win

def main():
    db = DBmanager("TodoList.db")
    window = Win(db, (800, 600), "#F7F9FB")
    window.show()
    return 1

if __name__ == "__main__":
    main()
