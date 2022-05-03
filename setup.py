# setup.py by CoccaGuo at 2022/04/29 19:02

import os
from app import STATIC_FILE_LIST


# setup static file path

for path in STATIC_FILE_LIST:
    if not os.path.exists(os.path.join('static', path)):
        os.mkdir(os.path.join('static', path))


