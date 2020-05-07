import shlex
from subprocess import Popen, call, check_output, CalledProcessError
from django.core.management.base import BaseCommand
from django.utils import autoreload
import signal
import os

from event_manager.settings import DEBUG


def restart_server():
    if not DEBUG:
        cmd = 'python3 manage.py makemigrations'
        call(shlex.split(cmd))
        cmd = 'python3 manage.py migrate'
        call(shlex.split(cmd))
    cmd = 'rm -rf static_root'
    call(shlex.split(cmd))
    cmd = 'python3 manage.py collectstatic'
    call(shlex.split(cmd))
    cmd = 'pkill -f "celery worker"'
    call(shlex.split(cmd))
    cmd = 'pkill -f celery'
    call(shlex.split(cmd))
    try:
        process = check_output(["lsof", "-i", ":8000"])
        for process in str(process.decode("utf-8")).split("\n")[1:]:
            data = [x for x in process.split(" ") if x != '']
            if len(data) <= 1:
                continue

            os.kill(int(data[1]), signal.SIGKILL)
    except CalledProcessError:
        pass
    cmd = 'gunicorn -b 0.0.0.0:8000 event_manager.wsgi'
    Popen(shlex.split(cmd))
    cmd = 'celery worker -l info -A event_manager -c 2'
    Popen(shlex.split(cmd))


class Command(BaseCommand):

    def handle(self, *args, **options):
        autoreload.run_with_reloader(restart_server)
