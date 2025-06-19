from abc import ABC, abstractmethod
import sqlite3
import tkinter as tk
import tkinter.font as tkFont


# This class is a prototype for the following ones. It will be inherited by others, and the methods of this class are described abstractly via the @abstractmethod decorator. This requires that each abstract method must be implemented in child classes. It's similar to a virtual function in C++. Also, you cannot create an instance of a class with abstract methods inside.
# Abstract class -- interface
class IDbase(ABC):
    @abstractmethod
    def create_base(self) -> None: # -> annotation None means the method returns nothing
        pass

    @abstractmethod
    def add_task(self, title: str, description: str) -> bool: # annotation -> bool means the method returns true or false
        pass

    @abstractmethod
    def get_all_tasks(self) -> list[tuple]: # -> list[Tuple] annotation means the method returns a list of tuples
        pass




class DBmanager(IDbase):
    def __init__(self, dbname: str):
        self.connect = sqlite3.connect(dbname) # set up the DB
        self.cursor = self.connect.cursor() # set up the cursor
        self.create_base() # call the creation function directly from the constructor
    
    def __del__(self):
        self.connect.close() # close DB access when the program stops

   
    def create_base(self) -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks( 
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT NOT NULL
                            )''') # create the database itself
        self.connect.commit() # save state
    
    def add_task(self, title: str, description: str) -> bool:
        try:
            self.cursor.execute('''INSERT INTO tasks (title, description) VALUES (?, ?)''', (title, description)) # INSERT INTO TASKS (VALUE 1, VALUE 2) with values (function parameters and what we need)
            self.connect.commit()  # save state
            return True
        except sqlite3.Error as a:
            print(f"Error adding task {a}")
            return False
        
    def get_all_tasks(self) -> list[tuple]:
        try:
            self.cursor.execute('''SELECT * FROM tasks''') # command to give user access to all selects from DB
            self.connect.commit() # save state
            return self.cursor.fetchall() # returns a list of all elements in the DB
        except sqlite3.Error as a:
            print(f"Error is {a}") # default error handler

    def clear_all_tasks(self) -> bool:
        """Удаляет все задачи из базы данных"""
        try:
            self.cursor.execute('DELETE FROM tasks')
            self.connect.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error clearing tasks: {e}")
            return False

    def export_tasks_to_txt(self, filename: str = "tasks_export.txt") -> bool:
        """Экспортирует все задачи в текстовый файл"""
        try:
            tasks = self.get_all_tasks()
            with open(filename, 'w', encoding='utf-8') as f:
                for task in tasks:
                    f.write(f"ID: {task[0]}\nЗаголовок: {task[1]}\nОписание: {task[2]}\n---\n")
            return True
        except Exception as e:
            print(f"Error exporting tasks: {e}")
            return False


class Win:
    def __init__(self, todo_list: DBmanager, size: tuple[int, int], bg_color: str = "#F7F9FB"):
        """
        Initialize the window with todo list manager
        Args:
            todo_list: Database manager instance
            size: Window size as (width, height)
            bg_color: Background color in hex format
        """
        self.window = tk.Tk()
        self.todo_list = todo_list
        self.window.title("📝 Modern Todo List")
        self.window.geometry(f"{size[0]}x{size[1]}")
        self.window.configure(bg=bg_color)
        self.window.resizable(False, False)
        # self.window.option_add("*Font", default_font)
        self.window.option_add("*Button.Relief", "flat")
        self.window.option_add("*Button.BorderWidth", 0)
        self.window.option_add("*Entry.Relief", "flat")
        self.window.option_add("*Entry.BorderWidth", 2)
        self.window.option_add("*Listbox.Relief", "flat")
        self.window.option_add("*Listbox.BorderWidth", 2)
        # self.window.option_add("*Label.Font", "Segoe UI 12 bold")
        self.window.option_add("*Label.Background", bg_color)
        self.window.option_add("*Label.Foreground", "#222")
        self.window.option_add("*Entry.Background", "#fff")
        self.window.option_add("*Entry.Foreground", "#222")
        self.window.option_add("*Listbox.Background", "#fff")
        self.window.option_add("*Listbox.Foreground", "#222")
        self.window.option_add("*Button.Background", "#4CAF50")
        self.window.option_add("*Button.Foreground", "white")
        self.window.option_add("*Button.ActiveBackground", "#388E3C")
        self.window.option_add("*Button.ActiveForeground", "white")
        self.window.option_add("*HighlightThickness", 0)
        # Configure grid weights
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        # Create main frame
        self.main_frame = tk.Frame(self.window, bg=bg_color, bd=0, highlightthickness=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        # Create left and right frames
        self.left_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.right_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.right_frame.grid(row=0, column=1, sticky="n")
        # Create widgets
        self.create_widgets()
        self.create_input_widgets()
        
    def create_widgets(self):
        """Create and initialize all widgets"""
        # Title label
        self.title_label = tk.Label(
            self.left_frame,
            text="📝 Todo List",
            font=("Segoe UI", 20, "bold"),
            bg=self.window["bg"],
            fg="#222"
        )
        self.title_label.grid(row=0, column=0, pady=(0, 18))
        
        # Tasks list
        self.tasks_listbox = tk.Listbox(
            self.left_frame,
            width=48,
            height=18,
            font=("Segoe UI", 11),
            bg="#fff",
            fg="#222",
            bd=0,
            highlightthickness=1,
            highlightcolor="#E0E0E0",
            selectbackground="#E3F2FD",
            selectforeground="#1976D2",
            relief="flat"
        )
        self.tasks_listbox.grid(row=1, column=0, pady=10, ipady=4)
        
        # Update tasks display
        self.update_tasks()

    def create_input_widgets(self):
        """Create input widgets"""
        # Styles for input fields
        entry_style = {
            'width': 24,
            'font': ('Segoe UI', 11),
            'bg': '#F5F5F5',
            'fg': '#222',
            'bd': 0,
            'highlightthickness': 1,
            'highlightcolor': '#90CAF9',
            'relief': 'flat',
            'insertbackground': '#1976D2'
        }
        
        # Styles for button
        button_style = {
            'width': 16,
            'height': 2,
            'font': ('Segoe UI', 11, 'bold'),
            'bd': 0,
            'relief': 'flat',
            'activebackground': '#388E3C',
            'activeforeground': 'white',
            'cursor': 'hand2',
        }

        # Label for title
        title_label = tk.Label(self.right_frame, text="Заголовок:", font=("Segoe UI", 11, "bold"), anchor="w")
        title_label.grid(row=0, column=0, pady=(0, 4), sticky="w")
        
        # Field for title
        self.title_entry = tk.Entry(self.right_frame, **entry_style)
        self.title_entry.grid(row=1, column=0, pady=4, ipady=4)
        
        # Label for description
        desc_label = tk.Label(self.right_frame, text="Описание:", font=("Segoe UI", 11, "bold"), anchor="w")
        desc_label.grid(row=2, column=0, pady=(12, 4), sticky="w")
        
        # Field for description
        self.description_entry = tk.Entry(self.right_frame, **entry_style)
        self.description_entry.grid(row=3, column=0, pady=4, ipady=4)
        
        # Add button
        self.add_button = tk.Button(
            self.right_frame,
            text="Добавить задачу",
            command=self.add_new_task,
            bg="#43A047",
            fg="white",
            **button_style
        )
        self.add_button.grid(row=4, column=0, pady=(14, 4))

        # Export button
        self.export_button = tk.Button(
            self.right_frame,
            text="Экспортировать задачи в .txt",
            command=self.export_tasks,
            bg="#1976D2",
            fg="white",
            **button_style
        )
        self.export_button.grid(row=5, column=0, pady=4)

        # Clear button
        self.clear_button = tk.Button(
            self.right_frame,
            text="Очистить все задачи",
            command=self.clear_tasks,
            bg="#D32F2F",
            fg="white",
            **button_style
        )
        self.clear_button.grid(row=6, column=0, pady=4)

    def add_new_task(self):
        """Handler for add task button click"""
        title = self.title_entry.get()
        description = self.description_entry.get()
        
        if title and description:
            if self.add_task(title, description):
                # Success message
                success_label = tk.Label(
                    self.right_frame,
                    text="Задача успешно добавлена!",
                    fg="green"
                )
                success_label.grid(row=7, column=0, pady=5)
                # Remove message after 2 seconds
                self.window.after(2000, success_label.destroy)
                
                # Clear fields after adding
                self.title_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
            else:
                # Error message
                error_label = tk.Label(
                    self.right_frame,
                    text="Ошибка при добавлении задачи!",
                    fg="red"
                )
                error_label.grid(row=7, column=0, pady=5)
                self.window.after(2000, error_label.destroy)
        else:
            # Message about empty fields
            error_label = tk.Label(
                self.right_frame,
                text="Заполните все поля!",
                fg="red"
            )
            error_label.grid(row=7, column=0, pady=5)
            self.window.after(2000, error_label.destroy)
        
    def update_tasks(self):
        """Update the tasks display"""
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
        Add a new task
        Args:
            title: Task title
            description: Task description
        Returns:
            bool: True if task was added successfully
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
        """Show the window and start the main loop"""
        self.window.mainloop()
        
    def __del__(self):
        """Cleanup when the window is destroyed"""
        try:
            self.window.destroy()
        except:
            pass

    def export_tasks(self):
        """Export tasks to txt file and show message"""
        if self.todo_list.export_tasks_to_txt():
            msg = tk.Label(self.right_frame, text="Задачи экспортированы!", fg="blue")
            msg.grid(row=7, column=0, pady=5)
            self.window.after(2000, msg.destroy)
        else:
            msg = tk.Label(self.right_frame, text="Ошибка экспорта!", fg="red")
            msg.grid(row=7, column=0, pady=5)
            self.window.after(2000, msg.destroy)

    def clear_tasks(self):
        """Clear all tasks and update the list"""
        if self.todo_list.clear_all_tasks():
            self.update_tasks()
            msg = tk.Label(self.right_frame, text="Все задачи удалены!", fg="red")
            msg.grid(row=7, column=0, pady=5)
            self.window.after(2000, msg.destroy)
        else:
            msg = tk.Label(self.right_frame, text="Ошибка очистки!", fg="red")
            msg.grid(row=7, column=0, pady=5)
            self.window.after(2000, msg.destroy)