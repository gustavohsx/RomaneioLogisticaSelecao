import sys
from cx_Freeze import setup, Executable

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="GeradorRomaneio",
    version="2.0",
    description="Programa Gerador de Romaneio",
    executables=[Executable("app.py", base=base)],
)