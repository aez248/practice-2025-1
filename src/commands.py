"""
Встроенные команды для Shell
"""

import os
import sys

def cmd_cd(args, shell):
    """Смена текущей директории"""
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

def cmd_exit(args, shell):
    """Выход из оболочки"""
    print("Выход...")
    sys.exit(0)

def cmd_help(args, shell):
    """Справка по командам"""
    help_text = """
Доступные команды:
  cd [dir]   — сменить текущую директорию
  exit       — выйти из оболочки
  help       — показать эту справку
  
Также можно запускать любые внешние программы (ls, pwd, echo и т.д.)
    """
    print(help_text)

def cmd_history(args, shell):
    """Показать историю команд"""
    for i, cmd in enumerate(shell.history, 1):
        print(f"{i:4}  {cmd}")

builtin_commands = {
    "cd": cmd_cd,
    "exit": cmd_exit,
    "help": cmd_help,
    "history": cmd_history,
}
