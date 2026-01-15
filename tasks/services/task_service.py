from contextlib import contextmanager
from typing import Generator
from django.db import transaction
from tasks.models import Task
from django.contrib.auth.models import User

@contextmanager
def atomic_task_creation() -> Generator[None, None, None]:
    with transaction.atomic():
        yield

def create_task(user: User, title: str) -> Task:
    with atomic_task_creation():
        task = Task.objects.create(user=user, title=title)
        return task

def user_tasks_generator(user: User):
    tasks = Task.objects.filter(user=user)
    for task in tasks.iterator():
        yield task