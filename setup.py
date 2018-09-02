from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = "C:\\Python\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python\\tcl\\tk8.6"

base = None
executables = [Executable("main.py", base=base)]

packages = ["idna", "functions", "time", "math", "pygame", "sys", "random", "os.path", 'classes']
buildOptions = dict(include_files = ['data/', 'images/', 'savefiles/', 'sounds/'])  #folder,relative path. Use tuple like in the single file to set a absolute path.


options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
         name = "Shape Defense",
         version = "1.0",
         description = "Tower Defense",
         author = "Tommy Huang",
         options = dict(build_exe = buildOptions),
         executables = executables)