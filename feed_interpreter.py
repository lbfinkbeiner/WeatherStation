"""
    File name: feed_interpreter.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/5/2021
    Python version: 3.7.3
"""

import re, os, enum, sys
import time as t
import numpy as np

class Role(enum.Enum):
    ignore = 0
    primary = 1
    comms = 2
# garbage import
import traceback

# Now back to semi-legitimate programming

def listen(full_feed, df1, df2):
    var_vals1 = {}
    var_vals2 = {}
    for var in var_abbrs.keys():
        var_vals1[var] = None
        var_vals2[var] = None
       
    while True:
        try:
            if full_feed["feed1"]["updated"]:
                handle(full_feed["feed1"], var_vals1, df1)
                post_diffs(full_feed, var_vals1, var_vals2)
            if full_feed["feed2"]["updated"]:
                handle(full_feed["feed2"], var_vals2, df2)
                post_diffs(full_feed, var_vals1, var_vals2)
 
        except Exception as e:
            print(e)
            traceback.print_exc()
            print("TKInter probably died. Please try again.")
            sys.exit()

def handle(feed, var_vals, df):
    print(df)

    feed["updated"] = False
    parse(feed["raw"], var_vals, df)
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

def parse(line, var_vals, df): 
    # This approach (recreating the data frame every time
    # we want to add a row) may prove computationally
    # infeasible for the Pi by the end of the day
    preexisting_times = list(df.index)
    final_row_index = t.time()
    new_index = preexisting_times + [final_row_index]
    df.reindex(new_index)

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

        df.at[final_row_index, var_name] = var_val

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
            
            # for demo purposes, we are hard-coding a data len cap of 10
            if var == "Ta":
                gd = full_feed["graph_data"]["Ta"]
                if gd["x"] is None:
                    gd["x"] = np.array([0])
                    gd["y"] = np.array([var_vals1[var]])
                elif gd["x"].size == 10:
                    gd["x"] = np.roll(gd["x"], -1)
                    gd["y"] = np.roll(gd["y"], -1)
                    gd["x"][9] = gd["x"][8] + 1
                    gd["y"][9] = var_vals1[var]
                else:
                    last_i = gd["x"].size - 1
                    last_x = gd["x"][last_i]
                    x_element = np.array([last_x + 1])
                    y_element = np.array([var_vals1[var]])
                    gd["x"] = np.append(gd["x"], x_element)
                    gd["y"] = np.append(gd["y"], y_element)
                 
                full_feed["graph_soul"]()

            styled += var_abbrs[var]
            styled += ": "
            styled += str(np.around(var_vals2[var] - var_vals1[var], 4))
            styled += default_units[var]
            styled += "\n"
    
    if full_feed["diff_soul"] is not None:
        full_feed["diff_soul"](styled)
