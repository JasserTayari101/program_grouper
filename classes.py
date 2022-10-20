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
    def __init__(self,run_type):
        super().__init__()
        self.os_name = os.name      #used for os specific operations (windows/linux)
        print(run_type)
        self.labels = (0,[])    #   used for keeping track of the list of labels and the current selected one indicated by an integer, might be changed to a linked list DS
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
        
        self.exe_btn = tk.Button(self.btn_frm,text="RUN",command=self.runfile)
        self.exe_btn.grid(row=0,column=1)
        
        self.all_btn = tk.Button(self.btn_frm,text="RUN ALL",command=lambda :self.runfile(runall=True))
        self.all_btn.grid(row=0,column=2)
        
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
        patterns = ("*.bash","*.sh","*.zsh") if self.os_name.lower() == "posix" else ("*.exe",)
        filename = filedialog.askopenfilename(initialdir="/",filetypes=(("executables",patterns),("any","*.*") ) )  #platform specific patterns
        if filename:
            lbl = tk.Label(self.container.scrollable_frame, text=filename)
            lbl.configure(bg=("white" if len(self.labels[1]) else "grey") )
            self.labels[1].append(lbl)
            lbl.pack()
    def runfile(self,runall=False):
        if runall:
            for lbl in self.labels[1]:
                name = lbl.cget("text")
                os.system("sh %s"%name)    
        else:
            curr = self.labels[0]
            current = (self.labels[1][curr]).cget("text")
            os.system("sh %s"%current)
    def destroy(self):
        super().destroy()



class Login(tk.Tk):     #a login interface used to select between guest/sign in/sign up by creating a json file
    def __init__(self):
        super().__init__()
        self.resizable(False,False)
        self.guest_btn = tk.Button(self,text="Login as guest",command=self.guest)
        self.guest_btn.pack()
        
        tk.Label(self,text="---------------------").pack()
        
        self.sign_in_btn = tk.Button(self,text="Sign in as existing user")
        self.sign_in_btn.pack()
        
        tk.Label(self,text="---------------------").pack()
        
        self.sign_up_btn = tk.Button(self,text="Create new user")
        self.sign_up_btn.pack()
    def guest(self):
        import json
        res = {"type":"guest"}
        with open("type.json","w") as f:
            json.dump(res,f)
        self.destroy()