# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///list.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.id


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def ask_menu():
    print("1) Today's tasks")
    print("2) Add task")
    print("0) Exit")

    choice = -1

    while choice > 2 or choice < 0:
        choice = int(input())

    return choice


def trigger_action(menu_choice: int):
    if menu_choice == 1:
        return todays_task()

    if menu_choice == 2:
        return add_task()

    return exit()


def exit():
    print('Bye!')


def print_todays_tasks(rows):
    row_index = 1
    for row in rows:
        print(f'{row_index}. {row.task}')
        row_index += 1


def todays_task():
    rows = session.query(Table).all()

    print('Today:')
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        print_todays_tasks(rows)


def add_task():
    task = input()
    new_row = Table(task=task)
    session.add(new_row)
    session.commit()


menu_choice = -1
while menu_choice != 0:
    menu_choice = ask_menu()
    trigger_action(menu_choice)
