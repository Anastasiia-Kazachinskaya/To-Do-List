from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')  # создание СУБД, обращение к ней

Base = declarative_base()  ##создание класса, к которму можно обратиться


class Task(Base):
    __tablename__ = 'task'  ##создание и название таблицы
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())



    def __str__(self):
        return f"{self.task}"


Base.metadata.create_all(engine)  ##передаем обьект engine

Session = sessionmaker(bind=engine)  ### запускаем процесс
session = Session()

task_1 = Task(task='to complete the to do list project')


# def get_all_tasks():
# return session.query(Task).all() ## возращаем все строки в данном сеансе


def create_task():  ###пользователь создает задание
    task = input("Enter task\n")
    deadline = input("Enter deadline\n")
    deadline = datetime.strptime(deadline, '%Y-%m-%d')
    task_obj = Task(task=task, deadline=deadline)
    session.add(task_obj)
    session.commit()
    print("The task has been added!")

    return task_obj


def print_all_tasks():
    dates = []
    print("All tasks:")
    tasks = session.query(Task).all()
    if tasks:
        for i, task in enumerate(tasks):  ## перечисление всех задач
            print(f"{i + 1}. {task}")
            dates = list(set(dates))
            dates.sort()
            index = 1
            for date in dates:
                tasks = session.query(Task).filter(Task.deadline == date).all()
                for task in tasks:
                    print(f"{index}. {task.task}. {date.strftime('%d %b')}")
                    index += 1
    else:
        print("Nothing to do!")
    print()


def print_weekly_tasks():
    today = datetime.today()
    for i in range(7):
        day = today + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        tasks = session.query(Task).filter(Task.deadline == day_str).all()
        date = day.strftime("%A %b %d")
        if len(tasks):
            print(date)
            for index, task in enumerate(tasks):
                print(f"{index + 1}. {task.task}")
        else:
            print(date)
            print("Nothing to do! ")
        print()


def print_today_tasks():
    today = datetime.today().strftime("%Y-%m-%d")
    tasks = session.query(Task).filter(Task.deadline == today).all()
    date = datetime.today().strftime("%d %b")
    if len(tasks):
        print(f"Today {date}")
        for index, task in enumerate(tasks):
            print(f"{index + 1}. {task.task}")
    else:
        print(f"Today {date}")
        print("Nothing to do!")
    print()


def perform(choice):  # функция выбора пользователя
    if choice == "1":
        print_today_tasks()
    elif choice == "2":
        print_weekly_tasks()
    elif choice == "3":
        print_all_tasks()
    elif choice == "4":
        create_task()
    elif choice == "0":
        print("Bye!")
        exit()


while True:  # печатай, пока не выйдет
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Add task")
    print("0) Exit")
    choice = input()
    print()
    perform(choice)