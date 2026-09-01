#!/usr/bin/env python3
"""
Build your own Shell
Главный файл для запуска командной оболочки
"""

import sys
from shell import Shell

def main():
    shell = Shell()
    try:
        shell.run()
    except KeyboardInterrupt:
        print("\nВыход...")
        sys.exit(0)

if __name__ == "__main__":
    main()
