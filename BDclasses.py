from abc import ABC, abstractmethod
import sqlite3
import tkinter as tk


'''
'''
#абстрактный класс -- интерфейс
class IDbase(ABC):
    @abstractmethod
    def create_base(self) -> None: # -> аннотация None означает, что метод ничего не вернет
        pass

    @abstractmethod
    def add_task(self, title: str, description: str) -> bool: # это аннотации. -> bool значит, что метод вернет true or false 
        pass

    @abstractmethod
    def get_all_tasks(self) -> list[tuple]: # -> list[Tuple] аннотация означает, что метод будет возвращать список кортежей
        pass



'''
    в этом классе происхордит конкретная реализация всех методов от родительского класса IDbase
'''
class DBmanager(IDbase):
    def __init__(self, dbname: str):
        self.connect = sqlite3.connect(dbname) # задание ДБ.
        self.cursor = self.connect.cursor() # задание курсора
        self.create_base() # вызов функции создания напрямую из конструктора
    
    def __del__(self):
        self.connect.close() # закрытие доступа к бд-шке в момент остановки программы 

    # эта функция по аннотации ничего не должная возвращать, так что никакого return чего то там
    def create_base(self) -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks( 
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT NOT NULL
                            )''') # создания самой базы данных
        self.connect.commit() # сохранение состояния
    
    # эта функция по аннотации возвращает булевы значения
    def add_task(self, title: str, description: str) -> bool:
        try:
            self.cursor.execute('''INSERT INTO tasks (title, description) VALUES (?, ?)''', (title, description)) # ДОСТАТТЬ ИЗ TASKS (VALUE 1, VALUE 2) СО ЗНАЧЕНИЯМИ (ПАРАМЕТРЫ ФУНКЦИИ И ПРОСТО ТО, ЧТО НАМ НЕОБХОДИМО)
            self.connect.commit()  # сохранение состояния
            return True
        except sqlite3.Error as a:
            print(f"Error adding task {a}")
            return False
        
    # эта функция по анотации должна возвращать список кортежей, то есть как раз таки список всех элементов дб-шки
    def get_all_tasks(self) -> list[tuple]:
        try:
            self.cursor.execute('''SELECT * FROM tasks''') # это команда для того, чтобы открыть доступ пользователю ко всем селектам из дб
            self.connect.commit() # сохранение состаяния
            return self.cursor.fetchall() # возвращает список всех элементов в дб.
        except sqlite3.Error as a:
            print(f"Error is {a}") # дефолт обработчик ошибок


class Win:
    def __init__(self, todo_list: DBmanager, size: tuple[int, int], bg_color: str = "#FFFFFF"):
        """
        """
        self.window = tk.Tk()
        self.todo_list = todo_list
        self.window.geometry(f"{size[0]}x{size[1]}")
        self.window.configure(bg=bg_color)
        
        # Configure grid weights
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = tk.Frame(self.window, bg=bg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create widgets
        self.create_widgets()
        self.create_input_widgets()
        
    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(
            self.main_frame,
            text="Todo List",
            font=("Arial", 16, "bold"),
            bg=self.window["bg"]
        )
        self.title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Tasks list
        self.tasks_listbox = tk.Listbox(
            self.main_frame,
            width=50,
            height=15,
            font=("Arial", 10)
        )
        self.tasks_listbox.grid(row=1, column=0, pady=10)
        
        # Update tasks display
        self.update_tasks()

    def create_input_widgets(self):
        """Создание виджетов для ввода данных"""
        # Стили для полей ввода
        entry_style = {
            'width': 40,
            'font': ('Arial', 10)
        }
        
        # Стили для кнопки
        button_style = {
            'width': 20,
            'height': 2,
            'font': ('Arial', 10, 'bold'),
            'bg': '#4CAF50',
            'fg': 'white'
        }

        # Метка для заголовка
        title_label = tk.Label(self.main_frame, text="Заголовок:")
        title_label.grid(row=2, column=0, pady=(10,0))
        
        # Поле для заголовка
        self.title_entry = tk.Entry(self.main_frame, **entry_style)
        self.title_entry.grid(row=2, column=0, pady=5)
        
        # Метка для описания
        desc_label = tk.Label(self.main_frame, text="Описание:")
        desc_label.grid(row=3, column=0, pady=(10,0))
        
        # Поле для описания
        self.description_entry = tk.Entry(self.main_frame, **entry_style)
        self.description_entry.grid(row=3, column=0, pady=5)
        
        # Кнопка добавления
        self.add_button = tk.Button(
            self.main_frame,
            text="Добавить задачу",
            command=self.add_new_task,
            **button_style
        )
        self.add_button.grid(row=4, column=0, pady=10)

    def add_new_task(self):
        """Обработчик нажатия кнопки добавления задачи"""
        title = self.title_entry.get()
        description = self.description_entry.get()
        
        if title and description:
            if self.add_task(title, description):
                # Сообщение об успехе
                success_label = tk.Label(
                    self.main_frame,
                    text="Задача успешно добавлена!",
                    fg="green"
                )
                success_label.grid(row=5, column=0, pady=5)
                # Удаляем сообщение через 2 секунды
                self.window.after(2000, success_label.destroy)
                
                # Очистка полей после добавления
                self.title_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
            else:
                # Сообщение об ошибке
                error_label = tk.Label(
                    self.main_frame,
                    text="Ошибка при добавлении задачи!",
                    fg="red"
                )
                error_label.grid(row=5, column=0, pady=5)
                self.window.after(2000, error_label.destroy)
        else:
            # Сообщение о пустых полях
            error_label = tk.Label(
                self.main_frame,
                text="Заполните все поля!",
                fg="red"
            )
            error_label.grid(row=5, column=0, pady=5)
            self.window.after(2000, error_label.destroy)
        
    def update_tasks(self):
        """Обновление окна обнов"""
        try:
            # Clear current items
            self.tasks_listbox.delete(0, tk.END)
            
            # Get and display tasks
            tasks = self.todo_list.get_all_tasks()
            if not tasks:
                self.tasks_listbox.insert(tk.END, "No tasks yet")
            else:
                for task in tasks:
                    self.tasks_listbox.insert(tk.END, f"{task[1]}: {task[2]}")
        except Exception as e:
            print(f"Error updating tasks: {e}")
            
    def add_task(self, title: str, description: str = "") -> bool:
        """
            добавление новое задачи
        """
        try:
            if self.todo_list.add_task(title, description):
                self.update_tasks()
                return True
            return False
        except Exception as e:
            print(f"Error adding task: {e}")
            return False
            
    def show(self):
        """показывать окно"""
        self.window.mainloop()
        
    def __del__(self):
        """деструктор"""
        try:
            self.window.destroy()
        except:
            pass
