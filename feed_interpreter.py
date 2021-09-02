"""
    File name: feed_interpreter.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/2/2021
    Python version: 3.7.3
"""

import re, os, enum, sys
import numpy as np

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
    "Th": Role.ignore, #! double check this one, could go in comms
    "Vh": Role.comms,
    "Vs": Role.comms,
    "Vr": Role.ignore #! double check this one, could go in comms
}

# garbage import
import traceback

# Now back to semi-legitimate programming

def listen(full_feed):
    var_vals1 = {}
    var_vals2 = {}
    for var in var_abbrs.keys():
        var_vals1[var] = None
        var_vals2[var] = None
       
    stupid_counter = 0   
    while True:
        try:
            if full_feed["feed1"]["updated"]:
                stupid_counter += 1
                handle(full_feed["feed1"], var_vals1)
                post_diffs(full_feed, var_vals1, var_vals2)
            if full_feed["feed2"]["updated"]:
                stupid_counter += 1
                handle(full_feed["feed2"], var_vals2)
                post_diffs(full_feed, var_vals1, var_vals2)

            if stupid_counter == 2:
                t = np.arange(0, 3, 0.01)
                full_feed["graph_soul"](-2 * np.log(2 * np.pi * t + 1))
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            print("TKInter probably died. Please try again.")
            sys.exit()

def handle(feed, var_vals):
    feed["updated"] = False
    parse(feed["raw"], var_vals)
    primary_styled = ""
    comm_styled = ""
    
    for var in var_abbrs.keys():
        if var_roles[var] is Role.ignore:
            continue
        styled_line = var_abbrs[var]
        styled_line += ": "
        styled_line += str(var_vals[var])
        styled_line += default_units[var]
        styled_line += "\n"
        if var_roles[var] is Role.primary:
            primary_styled += styled_line
        elif var_roles[var] is Role.comms:
            comm_styled += styled_line
    if feed["primary_soul"] is not None:
        feed["primary_soul"](primary_styled)
    if feed["comm_soul"] is not None:
        feed["comm_soul"](comm_styled)

def parse(line, var_vals):
    # Every line starts with a group ID about which we don't care
    comma_i = line.find(",")
    line = line[(comma_i + 1):]

    comma_i = line.find(",")
    while comma_i != -1:
        next_var = line[:comma_i]
        sides = next_var.split("=")
        var_name = sides[0]

        float_pattern = r"\d+(\.\d+)?"
        var_val = re.search(float_pattern, sides[1]).group(0)

        var_vals[var_name] = float(var_val)

        line = line[(comma_i + 1):]
        comma_i = line.find(",")

    # We just have one last variable to parse.
    # Unfortunately, it is not comma-delimited.
    equals_i = line.find("=")
    var_name = line[:equals_i]
    if var_name == "Id":
        return # we don't care about Id
    line = line[(equals_i + 1):]

    non_float_pattern = r"[^\d\.]"
    non_float_match = re.search(non_float_pattern, line)
    
    if non_float_match is None:
    # ad-hoc fix; I'm not sure what causes this
        return
    
    non_float_element = non_float_match.group(0)
    non_float_start_i = line.find(non_float_element)
    var_val = line[:non_float_start_i]

    try:
        var_vals[var_name] = float(var_val)
    except ValueError:
        print("Could not convert the following string to float:", var_val)
    
def post_diffs(full_feed, var_vals1, var_vals2):
    styled = ""
        
    for var in var_abbrs.keys():
        if var_roles[var] is not Role.ignore:
            if var_vals2[var] is None or var_vals1[var] is None:
                return
            styled += var_abbrs[var]
            styled += ": "
            styled += str(np.around(var_vals2[var] - var_vals1[var], 4))
            styled += default_units[var]
            styled += "\n"
    if full_feed["diff_soul"] is not None:
        full_feed["diff_soul"](styled)
