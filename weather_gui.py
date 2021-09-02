"""
    File name: weather_gui.py
    Author: Lukas Finkbeiner
    Date created: 8/31/2021
    Date last modified: 9/2/2021
    Python version: 3.7.3

    Credit to soumibardhan10 and
    Abhishek Goyal for the underlying
    structure of the application.
"""

import tkinter as tk
from tkinter import ttk

# This next import is currently for testing
# purposes and should be axed, maybe
import numpy as np

from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

LARGEFONT =("Verdana", 35)

feed = None

waiting = "waiting for data...\n" + \
          "this can typically take up to ten seconds"

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
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class WS1(tk.Frame):
    
    def __init__(self, parent, controller):
        def update(new_text):
            WS1_details.config(text = new_text)
        
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Weather Station 1", font = LARGEFONT)
        title.grid(row = 0, column = 2, padx = 10, pady = 10)
        
        WS1_details = ttk.Label(self, text = waiting)
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
  
        feed["feed1"]["primary_soul"] = update
  
class WS2(tk.Frame):
     
    def __init__(self, parent, controller):
        def update(new_text):
            WS2_details.config(text = new_text)
        
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Weather Station 2", font = LARGEFONT)
        title.grid(row = 0, column = 2, padx = 10, pady = 10)
  
        WS2_details = ttk.Label(self, text = waiting)
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
        
        feed["feed2"]["primary_soul"] = update
  
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
        
        diff_details = ttk.Label(self, text = waiting)
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
        
        feed["diff_soul"] = update
        
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
        
        WS1_details = ttk.Label(self, text = waiting)
        WS1_details.grid(row = 2, column = 2)
  
        button_WS1 = ttk.Button(self, text = "WS1",
            command = lambda : controller.show_frame(WS1))
        button_WS1.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        WS1_title = ttk.Label(self, text = "Weather Station 2")
        WS1_title.grid(row = 3, column = 2)
        
        WS2_details = ttk.Label(self, text = waiting)
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
        
        feed["feed1"]["comm_soul"] = update_WS1
        feed["feed2"]["comm_soul"] = update_WS2
        
class Graphs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
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

        # Here are some matplotlib tests

        fig = Figure(figsize=(5, 2), dpi=100)
        t = np.arange(0, 3, 0.01)
        fig.add_subplot().plot(t, 2 * np.sin(2 * np.pi * t))

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()

        canvas.get_tk_widget().grid(row=4, column=1, padx=10, pady=10)

        #canvas.get_tk_widget().pack(
        #        side=tk.TOP, fill=tk.BOTH, expand=1)

def start(input_feed):
    global feed
    feed = input_feed
    
    app = Weather_Interface()
    app.mainloop()
    
"""
We want 440 x 280, but
it automatically resizes;
I suppose we can work with that.
"""
