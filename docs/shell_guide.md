Техническое руководство: Создание собственной командной оболочки (Shell) на Python
1. Введение
Данное руководство описывает процесс создания простой командной оболочки (Shell) на языке Python. Проект выполнен в рамках вариативной части проектной (учебной) практики.

Цель руководства — показать, как устроены командные интерпретаторы изнутри, и дать практические навыки работы с системными вызовами, обработкой пользовательского ввода, организацией цикла команд и реализацией встроенных команд.

2. Что такое Shell?
Shell (командная оболочка) — это программа, которая принимает команды от пользователя (ввод с клавиатуры), интерпретирует их и выполняет соответствующие действия.

Примеры популярных оболочек:

bash (Linux/macOS)

zsh (macOS)

cmd (Windows)

PowerShell (Windows)

Наша реализация повторяет базовые принципы этих программ, но в упрощённом виде.

3. Архитектура проекта
Проект состоит из трёх модулей, каждый из которых отвечает за свою часть функциональности.

Модули:

main.py — точка входа. Создаёт экземпляр класса Shell и запускает его.

shell.py — основная логика: цикл ввода-вывода, выполнение команд, обработка ошибок.

commands.py — набор встроенных команд: cd, exit, help, history.

Структура:

src/
├── main.py # точка входа
├── shell.py # класс Shell
└── commands.py # встроенные команды

4. Описание классов и функций
Класс Shell:

history: список всех введённых команд

prompt: строка приглашения (по умолчанию "$ > ")

run(): запускает главный цикл оболочки

execute(command): выполняет переданную команду

Модуль commands.py содержит функции для встроенных команд:

cmd_cd(args, shell) — смена текущей директории

cmd_exit(args, shell) — выход из оболочки

cmd_help(args, shell) — вывод справки

cmd_history(args, shell) — вывод истории команд

Все встроенные команды собраны в словарь builtin_commands, который используется в shell.py для проверки, является ли команда встроенной.

5. Схема работы оболочки
Пользователь вводит команду в терминале.

Программа считывает ввод через input().

Команда добавляется в историю (history).

Выполняется парсинг: команда разбивается на имя и аргументы.

Проверяется, является ли команда встроенной (есть в словаре builtin_commands).

Если команда встроенная — вызывается соответствующая функция.

Если команда не встроенная — она запускается как внешняя программа через subprocess.run().

Результат выполнения (stdout или stderr) выводится пользователю.

Цикл повторяется с шага 1.

6. Пошаговая инструкция по созданию
Шаг 1. Создание класса Shell

class Shell:
def init(self):
self.history = []
self.prompt = "$ > "

Шаг 2. Главный цикл

def run(self):
while True:
try:
command = input(self.prompt).strip()
if not command:
continue
self.history.append(command)
self.execute(command)
except EOFError:
print("\nВыход...")
break
except KeyboardInterrupt:
print("\nВыход...")
break

Шаг 3. Обработка команд

def execute(self, command):
parts = command.split()
cmd = parts[0]
args = parts[1:] if len(parts) > 1 else []

if cmd in builtin_commands:
builtin_commands[cmd](args, self)
return

try:
result = subprocess.run([cmd] + args, capture_output=True, text=True)
if result.stdout:
print(result.stdout, end='')
if result.stderr:
print(result.stderr, end='', file=sys.stderr)
except FileNotFoundError:
print(f"Команда не найдена: {cmd}", file=sys.stderr)
except Exception as e:
print(f"Ошибка: {e}", file=sys.stderr)

Шаг 4. Реализация встроенных команд (commands.py)

Команда cd — смена директории:

def cmd_cd(args, shell):
if not args:
target = os.path.expanduser("~")
else:
target = args[0]
try:
os.chdir(target)
except FileNotFoundError:
print(f"Директория не найдена: {target}", file=sys.stderr)
except NotADirectoryError:
print(f"Не является директорией: {target}", file=sys.stderr)
except PermissionError:
print(f"Нет доступа к: {target}", file=sys.stderr)

Команда exit — выход:

def cmd_exit(args, shell):
print("Выход...")
sys.exit(0)

Команда help — справка:

def cmd_help(args, shell):
help_text = """
Доступные команды:
cd [dir] — сменить текущую директорию
exit — выйти из оболочки
help — показать эту справку
history — показать историю команд

Также можно запускать любые внешние программы (ls, pwd, echo и т.д.)
"""
print(help_text)

Команда history — история команд:

def cmd_history(args, shell):
for i, cmd in enumerate(shell.history, 1):
print(f"{i:4} {cmd}")

Шаг 5. Регистрация команд в словаре

builtin_commands = {
"cd": cmd_cd,
"exit": cmd_exit,
"help": cmd_help,
"history": cmd_history,
}

Шаг 6. Точка входа (main.py)

#!/usr/bin/env python3
import sys
from shell import Shell

def main():
shell = Shell()
try:
shell.run()
except KeyboardInterrupt:
print("\nВыход...")
sys.exit(0)

if name == "main":
main()

7. Пример работы программы
Запуск:

python src/main.py

Пример сессии:

$ > help
Доступные команды:
cd [dir] — сменить текущую директорию
exit — выйти из оболочки
help — показать эту справку
history — показать историю команд

Также можно запускать любые внешние программы (ls, pwd, echo и т.д.)

>
c
d
/
>cd/ > pwd
/
>
e
c
h
o
"
H
e
l
l
o
,
S
h
e
l
l
!
"
H
e
l
l
o
,
S
h
e
l
l
!
>echo"Hello,Shell!"Hello,Shell! > history
1 help
2 cd /
3 pwd
4 echo "Hello, Shell!"
$ > exit
Выход...

8. Возможные улучшения
После базовой реализации можно добавить:

Поддержка пайпов (|) — объединение нескольких команд.

Переменные окружения — поддержка 
P
A
T
H
,
PATH,HOME.

Автодополнение команд по нажатию Tab.

Выполнение сценариев (скриптов) из файлов.

Цветной вывод для улучшения читаемости.

9. Заключение
В ходе выполнения проекта была создана собственная командная оболочка на Python. Реализованы встроенные команды и механизм запуска внешних программ.

Руководство демонстрирует:

как устроены командные интерпретаторы;

как применять стандартную библиотеку Python для работы с системой;

как организовать простой, но расширяемый архитектурный подход.

Данный проект может служить отправной точкой для создания более сложных систем, таких как собственный язык сценариев или облегчённая версия bash.

10. Источники
Build your own Shell: https://github.com/codecrafters-io/build-your-own-x#build-your-own-shell

Документация Python: os — https://docs.python.org/3/library/os.html

Документация Python: subprocess — https://docs.python.org/3/library/subprocess.html
