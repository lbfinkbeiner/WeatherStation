"""
Credit to soumibardhan10 and Abhishek Goyal for the underlying
structure of the application.
"""

import tkinter as tk
from tkinter import ttk  
 
LARGEFONT =("Verdana", 35)

feed = None

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
        title.grid(row = 0, column = 4, padx = 10, pady = 10)
        
        WS1_details = ttk.Label(self, text = "<waiting for data>")
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
  
        feed["feed1"]["soul"] = update
  
class WS2(tk.Frame):
     
    def __init__(self, parent, controller):
        def update(new_text):
            WS2_details.config(text = new_text)
        
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Weather Station 2", font = LARGEFONT)
        title.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        WS2_details = ttk.Label(self, text = "<waiting for data>")
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
        
        feed["feed2"]["soul"] = update
  
# This frame will show the discrepancies between the readings of
# the two weather stations.
class Deltas(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Discrepancies", font = LARGEFONT)
        title.grid(row = 0, column = 4, padx = 10, pady = 10)
  
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
        
class Comms(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Communications", font = LARGEFONT)
        title.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button_WS1 = ttk.Button(self, text = "WS1",
            command = lambda : controller.show_frame(WS1))
        button_WS1.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        button_WS2 = ttk.Button(self, text ="WS2",
            command = lambda : controller.show_frame(WS2))
        button_WS2.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        button_deltas = ttk.Button(self, text = "Deltas",
            command = lambda : controller.show_frame(Deltas))
        button_deltas.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        button_graphs = ttk.Button(self, text = "Graphs",
        command = lambda : controller.show_frame(Graphs))
        button_graphs.grid(row = 4, column = 1, padx = 10, pady = 10)
        
class Graphs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        title = ttk.Label(self, text = "Real-time Graphs", font = LARGEFONT)
        title.grid(row = 0, column = 4, padx = 10, pady = 10)
  
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

def start(input_feed):
    global feed
    feed = input_feed
    
    app = Weather_Interface()
    app.mainloop()
    """
    print("Refresh called")
    while True:
        print("looping")
        if feed["styled_changed"]:
            print("I should be updating!")
            souls["WS1"](feed["styled"])
            feed["styled_changed"] = False
    """
# we want 440 x 280
# It automatically resizes, so I suppose we can work with that
