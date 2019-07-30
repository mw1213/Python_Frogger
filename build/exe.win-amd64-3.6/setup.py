#!/usr/bin/env python

from cx_Freeze import setup,Executable
setup(name="Frogger",
         version="1.0",
         description="as above",
         executables=[Executable("frogger_zaliczenie.py", icon="icon.ico")])
