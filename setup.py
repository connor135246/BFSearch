# setup

import sys

from cx_Freeze import setup, Executable


build_options = {'include_files': ["data", "gui", "lang", "logs"]}

base = 'Win32GUI' if sys.platform == 'win32' else None

setup(name='BFSearch',
      version = '1.0',
      description = 'Gen 4 Battle Frontier search',
      options = {'build_exe': build_options},
      executables = [Executable('launch.py', base = base, target_name = 'BFSearch')])
