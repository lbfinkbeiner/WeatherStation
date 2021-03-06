"""
    File name: weather_gui.py
    Author: Lukas Finkbeiner
    Date created: 8/31/2021
    Date last modified: 9/6/2021
    Python version: 3.7.3

    Credit to soumibardhan10 and
    Abhishek Goyal for the underlying
    structure of the application.
"""

import tkinter as tk
from tkinter import ttk

import logging
import math
import time as t

# This next import is currently for testing
# purposes and should be axed, maybe
import numpy as np

from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import shared as s

LARGEFONT =("Verdana", 35)

WAITING = "Waiting for data...\n" + \
          "this can typically take up to twenty seconds"

"""
This is a hard-coded dictionary which pads the y-axis limits
symmetrically, so that tiny deviations do not produce unreadable graphs.

Warning! This code is not ready for production because
it assumes that weather_gui knows about all of the different
weather variables. Maybe we can add a string list to the
full_feed dictionary, where each string is a variable label.
That seems like kind of a lame solution, because it is ad-hoc
and conceals theory from the programmer...

Important finalization note:
    as of 03.09.2021:1506 I am just making this
    dictionary up off of the top of my head.
    Alex may want to take a look at it to check off
    on the values.
"""
yap = {
    "Dn": 5, # superficially this seems like a good idea, but
    # it might look weird to have negative regions of the axis...
    "Dm": 5,
    "Dx": 5,
    "Sn": 2, # ditto
    "Sm": 2, # ditto
    "Sx": 2, # ditto
    "Ta": 1,
    "Ua": 1, # ditto
    "Pa": 10, # we should look at a demo graph to get a better sense of this
    "Rc": 1,
    "Rd": 20,
    "Ri": 1,
    "Hc": 60,
    "Hd": 20,
    "Hi": 30,
    "Rp": 2,
    "Hp": 2,
    "Th": 1,
    "Vh": 1.5,
    "Vs": 1.5,
    "Vr": 1.5
}

# This command will shut down the whole GUI.
# It needs to be filled in when the thread is called.
destroy = None

class Weather_Interface(tk.Tk):
     
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
         
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {} 
  
        for F in (WS1, WS2, Deltas, Comms, Graphs):
  
            frame = F(container, self)
  
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(WS1)

        #self.destroy()
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class WS1(tk.Frame):
    
    def __init__(self, parent, controller):
        def update(new_text):
            WS1_details.config(text = new_text)
       
        def close_tool():
            logging.info(str(int(t.time())) + ": graceful shutdown initiated.")

            s.shutting_down = True
            s.save_to_disk()
            global destroy
            destroy()

        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Weather Station 1", font = LARGEFONT)
        title.grid(row = 0, column = 2, padx = 10, pady = 10)
        
        WS1_details = ttk.Label(self, text = WAITING)
        WS1_details.grid(row = 2, column = 2)
  
        button_WS2 = ttk.Button(self, text = "WS2",
            command = lambda : controller.show_frame(WS2))
        button_WS2.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button_deltas = ttk.Button(self, text = "Deltas",
            command = lambda : controller.show_frame(Deltas))
        button_deltas.grid(row = 2, column = 1, padx = 10, pady = 10)
  
        button_comms = ttk.Button(self, text = "Comm.s",
            command = lambda : controller.show_frame(Comms))
        button_comms.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        button_graphs = ttk.Button(self, text = "Graphs",
            command = lambda : controller.show_frame(Graphs))
        button_graphs.grid(row = 4, column = 1, padx = 10, pady = 10)
 
        button_quit = ttk.Button(self, text = "Quit",
                command = close_tool)
        button_quit.grid(row = 5, column = 1, padx = 10, pady = 10)

        s.feed1["primary_soul"] = update
  
class WS2(tk.Frame):
     
    def __init__(self, parent, controller):
        def update(new_text):
            WS2_details.config(text = new_text)
        
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Weather Station 2", font = LARGEFONT)
        title.grid(row = 0, column = 2, padx = 10, pady = 10)
  
        WS2_details = ttk.Label(self, text = WAITING)
        WS2_details.grid(row = 2, column = 2)
  
        button_WS1 = ttk.Button(self, text = "WS1",
            command = lambda : controller.show_frame(WS1))
        button_WS1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button_deltas = ttk.Button(self, text = "Deltas",
            command = lambda : controller.show_frame(Deltas))
        button_deltas.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        button_comms = ttk.Button(self, text = "Comm.s",
            command = lambda : controller.show_frame(Comms))
        button_comms.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        button_graphs = ttk.Button(self, text = "Graphs",
            command = lambda : controller.show_frame(Graphs))
        button_graphs.grid(row = 4, column = 1, padx = 10, pady = 10)
        
        s.feed2["primary_soul"] = update
  
# This frame shows the discrepancies between
# the readings of the two weather stations.
class Deltas(tk.Frame):
    
    def __init__(self, parent, controller):
        def update(new_text):
            diff_details.config(text = new_text)
        
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Discrepancies", font = LARGEFONT)
        title.grid(row = 0, column = 2, padx = 10, pady = 10)
        
        note = ttk.Label(self, text = "WS2 readings minus WS1 readings")
        note.grid(row = 1, column = 2)
        
        diff_details = ttk.Label(self, text = WAITING)
        diff_details.grid(row = 2, column = 2)
  
        button_WS1 = ttk.Button(self, text = "WS1",
            command = lambda : controller.show_frame(WS1))
        button_WS1.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        button_WS2 = ttk.Button(self, text ="WS2",
            command = lambda : controller.show_frame(WS2))
        button_WS2.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        button_comms = ttk.Button(self, text = "Comm.s",
            command = lambda : controller.show_frame(Comms))
        button_comms.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        button_graphs = ttk.Button(self, text = "Graphs",
            command = lambda : controller.show_frame(Graphs))
        button_graphs.grid(row = 4, column = 1, padx = 10, pady = 10)
        
        s.diff_soul = update
        
class Comms(tk.Frame):
    
    def __init__(self, parent, controller):
        def update_WS1(new_text):
            WS1_details.config(text = new_text)
        
        def update_WS2(new_text):
            WS2_details.config(text = new_text)

        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Communications", font = LARGEFONT)
        title.grid(row = 0, column = 2, padx = 10, pady = 10)
        
        WS1_title = ttk.Label(self, text = "Weather Station 1")
        WS1_title.grid(row = 1, column = 2)
        
        WS1_details = ttk.Label(self, text = WAITING)
        WS1_details.grid(row = 2, column = 2)
  
        button_WS1 = ttk.Button(self, text = "WS1",
            command = lambda : controller.show_frame(WS1))
        button_WS1.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        WS1_title = ttk.Label(self, text = "Weather Station 2")
        WS1_title.grid(row = 3, column = 2)
        
        WS2_details = ttk.Label(self, text = WAITING)
        WS2_details.grid(row = 4, column = 2)
        
        button_WS2 = ttk.Button(self, text ="WS2",
            command = lambda : controller.show_frame(WS2))
        button_WS2.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        button_deltas = ttk.Button(self, text = "Deltas",
            command = lambda : controller.show_frame(Deltas))
        button_deltas.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        button_graphs = ttk.Button(self, text = "Graphs",
            command = lambda : controller.show_frame(Graphs))
        button_graphs.grid(row = 4, column = 1, padx = 10, pady = 10)

        button_dump = ttk.Button(self, text = "Dump", command=s.save_to_disk)
        button_dump.grid(row = 5, column = 1, padx = 10, pady = 10)

        s.feed1["comm_soul"] = update_WS1
        s.feed2["comm_soul"] = update_WS2
        
class Graphs(tk.Frame):

    def __init__(self, parent, controller):
        def update_graphs(num_points=10):
            df_graph = s.df1.tail(num_points).dropna()
            x = np.array(list(df_graph.index)) # this sucks and needs reformatting

            if x.size > 1:
                left = x.min() - 1
                right = x.max() + 1
            
            for var in valid_graphs:
                graph = gh[var]
                y = np.array(list(df_graph[var]))
                graph["line"].set_xdata(x)
                graph["line"].set_ydata(y)
                graph["canvas"].draw()
                
                # Autoscale is not working as expected,
                # so this is a work-around.
                if x.size > 1:
                    graph["ax"].set_xlim(left, right)
                    bottom = y.min() - yap[var]
                    top = y.max() + yap[var]
                    graph["ax"].set_ylim(bottom, top)
                
                graph["canvas"].flush_events()
       
        def next_page():
            self.graphs_page += 1
            update_visibilities()

        def prev_page():
            self.graphs_page -= 1
            update_visibilities()
        
        def update_visibilities():
            if self.graphs_page == 0:
                button_prev["state"] = "disabled"
            else:
                button_prev["state"] = "normal"
            if self.graphs_page == self.NUM_PAGES - 1:
                button_next["state"] = "disabled"
            else:
                button_next["state"] = "normal"

            for i in range(len(valid_graphs)):
                var = valid_graphs[i]
                if int(i / self.PAGE_SIZE) != self.graphs_page:
                    gh[var]["canvas"].get_tk_widget().grid_remove()
                else:
                    gh[var]["canvas"].get_tk_widget().grid()
        
        tk.Frame.__init__(self, parent)

        self.graphs_page = 0
        # the maximum number of graphs we think
        # can reasonably fit on a single page
        self.PAGE_SIZE = 2
        self.PLOT_SEPARATION = 2
        self.INIT_PLOT_ROW = 1

        valid_graphs = [key for key in s.var_abbrs.keys() \
                if key != "Dm" and s.var_roles[key] is not s.Role.ignore]
        self.NUM_PAGES = int(math.ceil(len(valid_graphs) / self.PAGE_SIZE))

        title = ttk.Label(self, text = "Real-time Graphs", font = LARGEFONT)
        title.grid(row = 0, column = 2, padx = 10, pady = 10)
  
        button_WS1 = ttk.Button(self, text = "WS1",
            command = lambda : controller.show_frame(WS1))
        button_WS1.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        button_WS2 = ttk.Button(self, text ="WS2",
            command = lambda : controller.show_frame(WS2))
        button_WS2.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        button_deltas = ttk.Button(self, text = "Deltas",
            command = lambda : controller.show_frame(Deltas))
        button_deltas.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        button_comms = ttk.Button(self, text = "Comm.s",
            command = lambda : controller.show_frame(Comms))
        button_comms.grid(row = 4, column = 1, padx = 10, pady = 10)

        button_prev = ttk.Button(self, text = "Previous",
            command = prev_page)
        button_prev.grid(row = 0, column=2, padx=10, pady=10)
        
        button_next = ttk.Button(self, text = "Next",
            command = next_page)
        button_next.grid(row = 0, column=4, padx=10, pady=10)

        # ! I think that a direction 1D plot would be difficult to read,
        # so I am not including it at the moment

        # "graph handles." It's a pretty extreme abbreviation,
        # but it's a sufficiently common label to warrant it.
        gh = {}

        for i in range(len(valid_graphs)):
            var = valid_graphs[i]
            gh[var] = {}
            
            gh[var]["fig"] = Figure(figsize=(5, 3), dpi=100)
            gh[var]["ax"] = gh[var]["fig"].add_subplot(111)
            
            title = s.var_abbrs[var] + " over Time"
            gh[var]["fig"].suptitle(title)
            gh[var]["ax"].set_xlabel("Time [index]")
            y_label = s.var_abbrs[var] + " [" + s.default_units[var] + "]"
            gh[var]["ax"].set_ylabel(y_label)
            gh[var]["fig"].tight_layout()

            # dummy starting plot to get useful handles
            t_dummy = np.arange(0, 3, 0.01)
            gh[var]["line"], = gh[var]["ax"].plot(t_dummy, 2 * np.sin(2 * np.pi * t_dummy))

            gh[var]["canvas"] = FigureCanvasTkAgg(gh[var]["fig"], self)
            gh[var]["canvas"].draw()

            row = self.INIT_PLOT_ROW
            if i % 2 == 1:
                row += self.PLOT_SEPARATION

            gh[var]["canvas"].get_tk_widget().grid(row=row, column=2, padx=10, pady=10)


        s.graph_soul = update_graphs

        update_visibilities()
       
        #scrollbar = tk.Scrollbar(self, orient="vertical")
        #scrollbar.config(yscrollcommand=gh["Sx"]["canvas"].yview)
        #scrollbar.grid(row=0, column=4, sticky="NSE")
def start():
    app = Weather_Interface()
    global destroy
    destroy = app.destroy
    app.mainloop()
    
"""
We want 440 x 280, but
it automatically resizes;
I suppose we can work with that.
"""

