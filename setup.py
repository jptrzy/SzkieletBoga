import cx_Freeze
from cx_Freeze import *

setup(
    name="SzkieletBoga",
    options = {'build_exe':{'packages': ['json', 'codecs'], 'include_files':['data']}},
    executables=[
        Executable(
            'SzkieletBoga.py'
        )
    ]
)
