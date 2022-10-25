import tkinter as tk
from tkinter import filedialog, Text
import os
import shelve
import json

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
    def __init__(self,res):
        super().__init__()
        self.os_name = os.name      #used for os specific operations (windows/linux)
        self.res = res
        self.run_type = res["type"]
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
        
        if self.run_type == "guest":
            try:
                self.data_file = open("data_file","r")      #when first opening the runner import the executables in data_file
                self.added_programs(self.data_file)                          #by adding them to the interface
            except FileNotFoundError:
                pass
            finally:
                self.data_file = open("data_file","a")      #then convert the open mode to append
        elif self.run_type == "user":
            self.added_programs(self.res["programs"])
        
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
    def added_programs(self,program_list):      #used to add existing labels in the data file
        for line in program_list:
            line = line.strip()
            lbl = tk.Label(self.container.scrollable_frame, text=line)
            lbl.configure(bg=("white" if len(self.labels[1]) else "grey") )
            self.labels[1].append(lbl)
            lbl.pack()
        
    def openfile(self):
        patterns = ("*.bash","*.sh","*.zsh") if self.os_name.lower() == "posix" else ("*.exe",)
        filename = filedialog.askopenfilename(initialdir=os.environ.get("HOME"),filetypes=(("executables",patterns),("any","*.*") ) )  #platform specific patterns
        if filename:
            lbl = tk.Label(self.container.scrollable_frame, text=filename)
            lbl.configure(bg=("white" if len(self.labels[1]) else "grey") )
            self.labels[1].append(lbl)
            if self.run_type == "guest":
                self.data_file.write(lbl.cget("text")+"\n")     # added the new program to the data file
            elif self.run_type == "user":
                self.res["programs"].append(lbl.cget("text") ) 
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
        if self.run_type == "user":
            with shelve.open("database") as db:     #update the user in the database
                name = self.res["name"]
                user = db[name]
                user["programs"] = self.res["programs"]
                db[name] = user
            with open("type.json","w") as f:
                json.dump(self.res,f)       #update type.json to include the new added programs
        super().destroy()


class Login(tk.Tk):     #a login interface used to select between guest/sign in/sign up by creating a json file
    def __init__(self):
        super().__init__()
        self.resizable(False,False)
        self.guest_btn = tk.Button(self,text="Login as guest",command=self.guest)
        self.guest_btn.pack()
        
        tk.Label(self,text="---------------------").pack()
        
        self.sign_in_btn = tk.Button(self,text="Sign in as existing user",command=self.sign_in)
        self.sign_in_btn.pack()
        
        tk.Label(self,text="---------------------").pack()
        
        self.sign_up_btn = tk.Button(self,text="Create new user")
        self.sign_up_btn.pack()
    def guest(self):
        res = {"type":"guest"}
        with open("type.json","w") as f:
            json.dump(res,f)
        self.destroy()
    def sign_in(self):
        self.login_window = tk.Tk()
        # self.login_window.resizable(False,False)
        
        tk.Label(self.login_window,text="username").grid(row=0,column=0)
        self.login_window.username = tk.Entry(self.login_window);self.login_window.username.grid(row=0,column=1)
        
        tk.Label(self.login_window,text="password").grid(row=1,column=0);
        self.login_window.password = tk.Entry(self.login_window,show="*");self.login_window.password.grid(row=1,column=1)
        
        self.login_window.error = tk.Label(self.login_window,text="");self.login_window.error.grid(row=2,column=0)
        
        self.login_window.submit = tk.Button(self.login_window,text="Sign in",command=self.verify);self.login_window.submit.grid(row=3,column=0)
        self.login_window.cancel = tk.Button(self.login_window,text="Cancel",command=self.login_window.destroy);self.login_window.cancel.grid(row=3,column=1)

        
    def verify(self):
        with shelve.open("database") as db:
            try:
                login_username = self.login_window.username.get()
                login_password = self.login_window.password.get()
                user = db[login_username]
                if user["password"] == login_password:
                    res = {"type":"user","name":login_username,"programs":user["programs"]}
                    with open("type.json","w") as f:
                        json.dump(res,f)
                    self.login_window.destroy()
                    self.destroy()
                else:
                    self.login_window.error.configure(text="Wrong password!")
            except KeyError:    #user don't exist
                self.login_window.error.configure(text="username don't exist!")
class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        