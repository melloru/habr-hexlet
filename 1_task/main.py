import time
import threading
from queue import Queue


class Server:
    def __init__(self, id):
        self.id = id
        self.current_task = None
        self.remaining_time = 0
        self.lock = threading.Lock()

    def assign_task(self, task):
        """Назначить задачу серверу"""
        with self.lock:
            self.current_task = task
            self.remaining_time = task.duration
            print(f"Задание с {task.duration} секундами выполнения направлено на Сервер {self.id}.")

    def execute_task(self):
        """Исполнить задачу на сервере (уменьшить оставшееся время)"""
        if self.current_task:
            while self.remaining_time > 0:
                time.sleep(1)
                self.remaining_time -= 1
            print(f"Сервер {self.id} завершил выполнение задания: {self.current_task.duration} сек.")
            self.current_task = None  # Освободить сервер после выполнения

    def is_free(self):
        """Проверить, свободен ли сервер"""
        return self.remaining_time <= 0


class Task:
    def __init__(self, duration):
        self.duration = duration


class DistributedSystem:
    """Класс распределенной системы"""

    def __init__(self, num_servers):
        self.servers = [Server(i + 1) for i in range(num_servers)]
        self.task_queue = Queue()

        threading.Thread(target=self.process_tasks, daemon=True).start()

    def add_task(self, duration):
        """Добавить новую задачу"""
        task = Task(duration)
        self.task_queue.put(task)
        self.assign_task()

    def assign_task(self):
        """Назначить задачу серверу с минимальной загрузкой"""
        for server in self.servers:
            if server.is_free() and not self.task_queue.empty():
                task = self.task_queue.get()
                server.assign_task(task)
                threading.Thread(target=server.execute_task, daemon=True).start()

    def process_tasks(self):
        """Обрабатывать задачи, когда серверы освобождаются"""
        while True:
            self.assign_task()
            time.sleep(1)

    def display_state(self):
        """Вывести состояние серверов и очередь"""
        print("Состояние серверов:")
        for server in self.servers:
            if server.current_task:
                print(f"Сервер {server.id}: выполняет задание (осталось {server.remaining_time} сек.)")
            else:
                print(f"Сервер {server.id}: пусто")
        print(f"Очередь заданий: {self.task_queue.qsize()} заданий(ий).")


def main():
    print("Добро пожаловать в симулятор распределенной системы.")
    num_servers = int(input("Введите количество серверов: "))
    system = DistributedSystem(num_servers)

    while True:
        command = input("Введите команду (добавить <время>, статус для состояния, выход): ")
        if command.startswith("добавить"):
            _, duration = command.split()
            system.add_task(int(duration))
        elif command == "статус":
            system.display_state()
        elif command == "выход":
            break
        else:
            print("Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()
