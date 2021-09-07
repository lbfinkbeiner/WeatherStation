"""
    File name: shared.py
    Author: Lukas Finkbeiner
    Date created: 9/5/2021
    Date last modified: 9/5/2021
    Python version: 3.7.3
"""

import enum
import time as t
from pathlib import Path
from datetime import datetime as dt
import pandas as pd

# The next two lines help with readibility for the third
HOUR = 3600
MINUTE = 60
AUTOSAVE_INTERVAL = 1 * MINUTE

class Role(enum.Enum):
    ignore = 0
    primary = 1
    comms = 2

"""
Brace yourself for hard-code city:
the first two dictionaries come from
the weather station manual and the
last comes from Dr. Alexander Pollak.
"""

var_abbrs = {
    "Dn": "Wind direction minimum",
    "Dm": "Wind direction average",
    "Dx": "Wind direction maximum",
    "Sn": "Wind speed minimum",
    "Sm": "Wind speed average",
    "Sx": "Wind speed maximum",
    "Ta": "Air temperature",
    "Ua": "Relative Humidity",
    "Pa": "Air pressure",
    "Rc": "Rain accumulation",
    "Rd": "Rain duration",
    "Ri": "Rain intensity",
    "Hc": "Hail accumulation",
    "Hd": "Hail duration",
    "Hi": "Hail intensity",
    "Rp": "Rain peak intensity",
    "Hp": "Hail peak intensity",
    "Th": "Heating temperature",
    "Vh": "Heating voltage",
    "Vs": "Supply voltage",
    "Vr": "3.5V reference voltage"
}

default_units = {
    "Dn": " degrees",
    "Dm": " degrees",
    "Dx": " degrees",
    "Sn": " m/s",
    "Sm": " m/s",
    "Sx": " m/s",
    "Ta": " deg C",
    "Ua": "%",
    "Pa": " hPa",
    "Rc": " mm",
    "Rd": " s",
    "Ri": " mm/h",
    "Hc": " hits/cc",
    "Hd": " s",
    "Hi": " hits/cc/h",
    "Rp": " mm/h",
    "Hp": " hits/cc/h",
    "Th": " deg C",
    "Vh": " V",
    "Vs": " V",
    "Vr": " V"
}

var_roles = {
    "Dn": Role.ignore,
    "Dm": Role.primary,
    "Dx": Role.ignore,
    "Sn": Role.ignore,
    "Sm": Role.primary,
    "Sx": Role.primary,
    "Ta": Role.primary,
    "Ua": Role.primary,
    "Pa": Role.primary,
    "Rc": Role.ignore,
    "Rd": Role.ignore,
    "Ri": Role.ignore,
    "Hc": Role.ignore,
    "Hd": Role.ignore,
    "Hi": Role.ignore,
    "Rp": Role.ignore,
    "Hp": Role.ignore,
    "Th": Role.ignore, #! double check this one; could go in comms
    "Vh": Role.comms,
    "Vs": Role.comms,
    "Vr": Role.ignore #! double check this one; could go in comms
}

"""
'soul' is just jargon I made up to describe a function
that updates a specific label on the GUI. Without
this strange work-around those functions are
entirely internal and difficult to see from here.
"""
feed1 = {"raw": "", "updated": False,
         "primary_soul": None, "comm_soul": None,
         "latest_index": None}
feed2 = {"raw": "", "updated": False,
         "primary_soul": None, "comm_soul": None,
         "latest_index": None}

diff_soul = None
graph_soul = None

# This is an obsolete format;
# modernize ASAP
graph_data = {
    "Ta": {
        "x": None,
        "y": None
    }
}

def current_records(mode='r'):
    """
    Returns the file handles for today's records,
        which are internally based on the current month and day.
    If the relevant directories do not exist, this
        function automatically generates them.
    """
    today = dt.today()
    current_year = str(today.year)
    current_month = today.strftime('%b')
    folder_path = "./records/" + current_year + "/" + current_month
    Path(folder_path).mkdir(parents=True, exist_ok=True)
   
    # does Alex want this in American or proper format?
    # for now, I'll assume disgusting American format
    file_prefix = folder_path + "/" + today.strftime("%m-%d-%Y") + "_WS"

    # Is it okay for me to put WS# in the file name?
    # Or would Alex prefer that I create separate directories for WS1 and WS2?
    f1 = open(file_prefix + "1.csv", mode)
    f2 = open(file_prefix + "2.csv", mode)

    return f1, f2

def save_to_disk():
    f1, f2 = current_records(mode='w+')
    df1.to_csv(f1, na_rep='NaN', header=True, index=True, line_terminator="\n")
    df2.to_csv(f2, na_rep='NaN', header=True, index=True, line_terminator="\n")

df_columns = [var for var in var_roles.keys() \
        if var_roles[var] is not Role.ignore]

df1 = pd.DataFrame(columns=df_columns)
df2 = pd.DataFrame(columns=df_columns)

last_autosave = t.time()

shutting_down = False

