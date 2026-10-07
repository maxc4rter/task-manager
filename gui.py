import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from classes import Task, TaskManager


# Класс главного окна приложения
class TaskManagerApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")
        self.setup_ui()

    # Создаём все элементы окна
    def setup_ui(self):
        # Поля ввода
        tk.Label(self.root, text="Название").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root, width=33)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Описание").grid(row=1, column=0)
        self.desc_text = tk.Text(self.root, height=3, width=30)
        self.desc_text.grid(row=1, column=1)

        tk.Label(self.root, text="Срок (ГГГГ-ММ-ДД)").grid(row=2, column=0)
        self.date_entry = tk.Entry(self.root, width=33)
        self.date_entry.grid(row=2, column=1)

        # Кнопки
        tk.Button(self.root, text="Добавить задачу", command=self.add_task).grid(row=3, column=0)
        tk.Button(self.root, text="Удалить задачу", command=self.delete_task).grid(row=3, column=1)

        # Список задач
        self.tasks_listbox = tk.Listbox(self.root, width=50)
        self.tasks_listbox.grid(row=4, column=0, columnspan=2)
        # При выборе задачи в списке показываем её описание
        self.tasks_listbox.bind("<<ListboxSelect>>", self.show_description)

        # Поле для показа описания выбранной задачи (только для чтения)
        tk.Label(self.root, text="Описание выбранной задачи:").grid(row=5, column=0, columnspan=2)
        self.desc_view = tk.Text(self.root, height=4, width=50, state="disabled")
        self.desc_view.grid(row=6, column=0, columnspan=2)

        self.update_listbox()

    # Кнопка "Добавить задачу"
    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get()

        if title == "" or description == "" or due_date == "":
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        # Проверяем, что дата записана правильно
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return

        task = Task(title, description, due_date)
        self.manager.add_task(task)
        self.update_listbox()
        self.clear_inputs()

    # Кнопка "Удалить задачу"
    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if len(selected) > 0:
            self.manager.delete_task(selected[0])
            self.update_listbox()
            self.set_description_view("")
        else:
            messagebox.showinfo("Подсказка", "Сначала выберите задачу в списке")

    # Показываем описание выбранной задачи
    def show_description(self, event):
        selected = self.tasks_listbox.curselection()
        if len(selected) > 0:
            task = self.manager.tasks[selected[0]]
            self.set_description_view(task.description)

    # Записываем текст в поле описания
    def set_description_view(self, text):
        self.desc_view.config(state="normal")
        self.desc_view.delete("1.0", tk.END)
        self.desc_view.insert("1.0", text)
        self.desc_view.config(state="disabled")

    # Заново заполняем список на экране
    def update_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.tasks_listbox.insert(tk.END, task.title + " (до " + task.due_date + ")")

    # Очищаем поля ввода после добавления
    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
