import classes,json,os.path as pth

if not pth.isfile("type.json"):     #type.json indicate the behavior of the runner if it does not exist we create the login interface
    login = classes.Login()
    login.mainloop()
    
with open("type.json","r") as f:
    res = json.load(f)
    try:
        run_type = res["type"]
        runner = classes.Runner(res)
        runner.mainloop()
    except KeyError:
        pass