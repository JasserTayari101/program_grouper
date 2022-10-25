import classes,json,os.path as pth

if not pth.isfile("type.json"):     #type.json indicate the behavior of the runner if it does not exist we create the login interface
    login = classes.Login()
    login.mainloop()
    
try:
    with open("type.json","r") as f:
        try:
            res = json.load(f)
            runner = classes.Runner(res)
            runner.mainloop()
        except KeyError:
            pass
except FileNotFoundError:
    print("No Login type chosen!")