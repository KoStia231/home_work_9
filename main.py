import subprocess


def main():
    """Запуск команды python manage.py runserver"""
    subprocess.run(['python', 'manage.py', 'runserver'])


if __name__ == '__main__':
    main()
    print("Сервер запущен")
