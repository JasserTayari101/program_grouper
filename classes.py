import tkinter as tk
from tkinter import filedialog, Text
import os

class ScrollFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class Runner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.labels = (0,[])    #   used for keeping track of the list of labels and the current selected one indicated by an integer
        self.resizable(False,False)
        self.rowconfigure(0,minsize=450,weight=1)
        self.rowconfigure(1,minsize=50)
        
        self.columnconfigure(0,weight=1,minsize=500)
        #           creating a scrollbar
        #------------------------------------
        self.container = ScrollFrame()

        self.container.grid(row=0,column=0,sticky="nsew")
        #---------------------------------------------------
        self.btn_frm = tk.Frame(self)
        self.btn_frm.grid(row=1,column=0,sticky="nsew")
        
        self.open_btn = tk.Button(self.btn_frm,text="Open File",command=self.openfile)
        self.open_btn.grid(row=0,column=0)
        
        self.exe_btn = tk.Button(self.btn_frm,text="RUN")
        self.exe_btn.grid(row=0,column=1)
        self.binding()
        
    def binding(self):        #create bindings for moving up and down
        self.bind("<Down>",lambda x:self.highlight_next(1))
        self.bind("<Up>",lambda x :self.highlight_next(-1))
    def highlight_next(self,increm):
        list_lbls = self.labels[1]
        curr = self.labels[0]   #the current selected label
        if  ( (increm==1) and (curr<len(list_lbls)-1 ) ) or ( (increm==-1) and (curr>0)):
            list_lbls[curr].configure(bg="white")
            curr+=increm
            list_lbls[curr].configure(bg="grey")
            self.labels = (curr,list_lbls)
    def openfile(self):
        filename = filedialog.askopenfilename(initialdir="/",filetypes=(("executables","*.sh"),("any","*.*") ) )
        if filename:
            lbl = tk.Label(self.container.scrollable_frame, text=filename)
            lbl.configure(bg=("white" if len(self.labels[1]) else "grey") )
            self.labels[1].append(lbl)
            lbl.pack()