"""
    File name: feed_interpreter.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/1/2021
    Python version: 3.7.3
"""

import re, os, enum

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
    "Th": Role.ignore, # double check this one, could go in comms
    "Vh": Role.comms,
    "Vs": Role.comms,
    "Vr": Role.ignore # double check this one, could go in comms
}


var_vals = {}

for var in var_abbrs.keys():
    var_vals[var] = None

# Now back to semi-legitimate programming

def listen(full_feed):
    while True: # gross
        if full_feed["feed1"]["updated"]:
            handle(full_feed["feed1"])
        if full_feed["feed2"]["updated"]:
            handle(full_feed["feed2"])

def handle(feed):
    feed["updated"] = False
    parse(feed["raw"])
    styled = ""
    
    for var in var_abbrs.keys():
        styled += var_abbrs[var]
        styled += ": "
        styled += str(var_vals[var])
        styled += default_units[var]
        styled += "\n"
    if feed["soul"] is not None:
        feed["soul"](styled)

def parse(line):
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
    # Unfortunately, it is not comma-delimited
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

    var_vals[var_name] = float(var_val)
