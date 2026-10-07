import json


# Класс одной задачи
class Task:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date


# Класс, который хранит список задач и работает с файлом
class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_from_file()

    # Добавляем задачу и сразу сохраняем в файл
    def add_task(self, task):
        self.tasks.append(task)
        self.save_to_file()

    # Удаляем задачу по номеру в списке
    def delete_task(self, index):
        if index >= 0 and index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()

    # Сохраняем все задачи в JSON-файл
    def save_to_file(self):
        data = []
        for task in self.tasks:
            item = {}
            item["title"] = task.title
            item["description"] = task.description
            item["due_date"] = task.due_date
            data.append(item)

        f = open(self.filename, "w", encoding="utf-8")
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.close()

    # Загружаем задачи из файла при запуске
    def load_from_file(self):
        self.tasks = []
        try:
            f = open(self.filename, "r", encoding="utf-8")
            data = json.load(f)
            f.close()
            for item in data:
                task = Task(item["title"], item["description"], item["due_date"])
                self.tasks.append(task)
        except FileNotFoundError:
            # Файла ещё нет - начинаем с пустого списка
            self.tasks = []
        except json.JSONDecodeError:
            # Файл пустой или повреждён - тоже начинаем с пустого списка
            self.tasks = []
