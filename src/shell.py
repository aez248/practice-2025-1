"""
Основная логика командной оболочки
"""

import os
import sys
import subprocess
from commands import builtin_commands

class Shell:
    def __init__(self):
        self.history = []
        self.prompt = "$ > "

    def run(self):
        """Главный цикл оболочки"""
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

    def execute(self, command):
        """Выполнение команды"""
        parts = command.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in builtin_commands:
            builtin_commands[cmd](args, self)
            return
        
        try:
            result = subprocess.run(
                [cmd] + args,
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, end='', file=sys.stderr)
        except FileNotFoundError:
            print(f"Команда не найдена: {cmd}", file=sys.stderr)
        except Exception as e:
            print(f"Ошибка: {e}", file=sys.stderr)
