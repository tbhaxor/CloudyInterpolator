import sys


def is_server_running() -> bool:
    is_gunicorn = sys.argv[0].endswith('gunicorn')
    is_dev = sys.argv[0].endswith('manage.py') and len(sys.argv) > 1 and sys.argv[1] == 'runserver'
    return is_gunicorn or is_dev


def is_test_running() -> bool:
    return sys.argv[0].endswith('manage.py') and len(sys.argv) > 1 and sys.argv[1] == 'test'


def is_test_or_server_running() -> bool:
    return is_test_running() or is_server_running()
