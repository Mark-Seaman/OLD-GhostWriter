from publish.days import recent_dates
from publish.text import text_join, text_lines
from task.models import Task
from task.task import fix_tasks, task_command


def test_task_recent():
    return text_join(recent_dates(30))


def test_task_records():
    text = task_command(['week', '2023-02-01', 'activity'])
    return f'Task Script:  {len(text_lines(text))} lines in summary'


def test_task_fix():
    fix_tasks()
    return 'OK'
