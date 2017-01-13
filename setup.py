from distutils.core import setup
import py2exe

setup(windows=[{'script':'Main.py','icon_resources':[(1,'stockmarket.ico')],"dest_base":"NexusMont"}],
      options = {"py2exe":{"dll_excludes":["MSVCP90.dll"]}},
      zipfile = None
      )