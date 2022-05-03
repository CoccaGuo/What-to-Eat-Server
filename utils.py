# utils.py by CoccaGuo at 2022/04/29 13:54

import time
import uuid
from werkzeug.utils import secure_filename

def unique_name(filename):
    """
    Generate a unique name for uploaded file
    """
    return str(time.time()) + '_' + secure_filename(filename)

def time_stamp():
    """
    Generate a time stamp
    """
    return str(int(time.time()*100))

# get a 3 digit random number by uuid
# because of the limitation of JavaScript's int length
def random_number():
    return str(uuid.uuid4().int)[:3]


def object_id():
    return int(time_stamp()+random_number())
    

