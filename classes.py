import tkinter as tk
from tkinter import filedialog, Text
import os


class Runner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.labels = (0,[])
        self.rowconfigure(0,minsize=450,weight=1)
        self.rowconfigure(1,minsize=50)
        
        self.columnconfigure(0,weight=1,minsize=500)
        #           creating a scrollbar
        #------------------------------------
        self.container = tk.Frame(self)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        #for i in range(50):
        #    if(i==0):
        #        lbl = tk.Label(self.scrollable_frame, text="Sample scrolling label",bg="grey")
        #    else:    
        #        lbl = tk.Label(self.scrollable_frame, text="Sample scrolling label",bg="white")
        #    lbl.pack()
        #    self.labels[1].append(lbl)

        self.container.grid(row=0,column=0,sticky="nsew")
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side="right", fill=tk.Y)
        #---------------------------------------------------
        self.btn_frm = tk.Frame(self)
        self.btn_frm.grid(row=1,column=0,sticky="nsew")
        
        self.open_btn = tk.Button(self.btn_frm,text="Open File",command=self.openfile)
        self.open_btn.grid(row=0,column=0)
        
        self.exe_btn = tk.Button(self.btn_frm,text="RUN")
        self.exe_btn.grid(row=0,column=1)
        self.binding()
    def binding(self):        #create bindings
        self.bind("<Down>",lambda x:self.highlight_next(1))
        self.bind("<Up>",lambda x :self.highlight_next(-1))
    def highlight_next(self,increm):
        list_lbls = self.labels[1]
        curr = self.labels[0]
        if  ( (increm==1) and (curr<len(list_lbls)-1 ) ) or ( (increm==-1) and (curr>0)):
            list_lbls[curr].configure(bg="white")
            curr+=increm
            list_lbls[curr].configure(bg="grey")
            self.labels = (curr,list_lbls)
    def openfile(self):
        filename = filedialog.askopenfilename(initialdir="/",filetypes=(("executables","*.sh"),("any","*.*") ) )
        if filename:
            print("entered")
            lbl = tk.Label(self.scrollable_frame, text=filename)
            lbl.configure(bg=("white" if len(self.labels[1]) else "grey") )
            self.labels[1].append(lbl)
            lbl.pack()