"""
    File name: feed_interpreter.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/6/2021
    Python version: 3.7.3
"""

import re, os, sys
import time as t
import numpy as np
import shared as s
# garbage import
import traceback

def listen():
    while not s.shutting_down:
        try:
            if s.feed1["updated"]:
                handle(s.feed1, s.df1)
                post_diffs()
            if s.feed2["updated"]:
                handle(s.feed2, s.df2)
                post_diffs()

            now = t.time()
            if now - s.last_autosave >= s.AUTOSAVE_INTERVAL:
                s.last_autosave = now
                s.save_to_disk()
 
        except Exception as e:
            print(e)
            traceback.print_exc()
            print("TKInter probably died. Please try again.")
            sys.exit()

def handle(feed, df):
    feed["updated"] = False
    parse(feed, df)
    primary_styled = ""
    comm_styled = ""

    for var in s.var_abbrs.keys():
        if s.var_roles[var] is s.Role.ignore:
            continue
        
        styled_line = s.var_abbrs[var]
        styled_line += ": "
        # we do not need to worry about this being None, because "updated" was marked True
        styled_line += str(df.loc[feed["latest_index"], var])
        styled_line += s.default_units[var]
        styled_line += "\n"
        
        if s.var_roles[var] is s.Role.primary:
            primary_styled += styled_line
        elif s.var_roles[var] is s.Role.comms:
            comm_styled += styled_line
    
    if feed["primary_soul"] is not None:
        feed["primary_soul"](primary_styled)
    
    if feed["comm_soul"] is not None:
        feed["comm_soul"](comm_styled)

def parse(feed, df): 
    # This approach (recreating the data frame every time
    # we want to add a row) may prove computationally
    # infeasible for the Pi by the end of the day
    line = feed["raw"]

    preexisting_times = list(df.index)
    new_index = preexisting_times + [feed["latest_index"]]
    df.reindex(new_index)

    # Every line starts with a group ID about which we don't care
    comma_i = line.find(",")
    line = line[(comma_i + 1):]

    comma_i = line.find(",")
    while comma_i != -1:
        next_var = line[:comma_i]
        sides = next_var.split("=")
        var_name = sides[0]

        if var_name in s.var_roles.keys() and \
                s.var_roles[var_name] is not s.Role.ignore:
            float_pattern = r"\d+(\.\d+)?"
            var_val = re.search(float_pattern, sides[1]).group(0)
    
            df.at[feed["latest_index"], var_name] = float(var_val)
    
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
        df.at[feed["latest_index"], var_name] = float(var_val)
    except ValueError:
        print("Could not convert the following string to float:", var_val)
    
def post_diffs():
    styled = ""
        
    for var in s.var_abbrs.keys():
        if s.var_roles[var] is not s.Role.ignore:
            try:
                val2 = s.df2.loc[s.feed2["latest_index"], var]
                val1 = s.df1.loc[s.feed1["latest_index"], var]
            except KeyError:
                return # not enough values yet to post differences

            if val2 is None or val1 is None:
                return
            if val2 is np.nan or val1 is np.nan:
                return

            # for demo purposes, we are hard-coding a data len cap of 10
            if var == "Ta":
                gd = s.graph_data["Ta"]
                if gd["x"] is None:
                    gd["x"] = np.array([0])
                    gd["y"] = np.array(val1)
                elif gd["x"].size == 10:
                    gd["x"] = np.roll(gd["x"], -1)
                    gd["y"] = np.roll(gd["y"], -1)
                    gd["x"][9] = gd["x"][8] + 1
                    gd["y"][9] = val1
                else:
                    last_i = gd["x"].size - 1
                    last_x = gd["x"][last_i]
                    x_element = np.array([last_x + 1])
                    y_element = np.array([val1])
                    gd["x"] = np.append(gd["x"], x_element)
                    gd["y"] = np.append(gd["y"], y_element)
                 
                s.graph_soul()

            styled += s.var_abbrs[var]
            styled += ": "
            styled += str(np.around(val2 - val1, 4))
            styled += s.default_units[var]
            styled += "\n"
    
    if s.diff_soul is not None:
        s.diff_soul(styled)

