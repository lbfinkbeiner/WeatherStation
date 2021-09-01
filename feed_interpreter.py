"""
    File name: telnet_interpret.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 8/31/2021
    Python version: 3.7.3
"""

import re, os

# Brace yourself for hard-code city

# Do we care about heating at all?

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

var_vals = {}

for var in var_abbrs.keys():
    var_vals[var] = None

# Now back to semi-legitimate programming

def listen(feed):
    while True: # gross
        if feed["raw_changed"]:
            feed["raw_changed"] = False
            #print(feed["value"])
            parse(feed["raw"])
            #os.system('clear') # clear screen
            feed["styled"] = ""
            for var in var_abbrs.keys():
                feed["styled"] += var_abbrs[var]
                feed["styled"] += ": "
                feed["styled"] += str(var_vals[var])
                feed["styled"] += default_units[var]
                feed["styled"] += "\n"
            feed["styled_changed"] = True
            if feed["souls"] is not None:
                #print("Attempting to update soul.")
                feed["souls"]["WS1"](feed["styled"])
            #else:
                #print("No souls available.")
            #print(feed["styled"])

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
