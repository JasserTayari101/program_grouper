import classes,json


try:
    with open("type.json","r") as f:
        res = json.load(f)
        try:
            run_type = res["type"]
            runner = classes.Runner(res)
            runner.mainloop()
        except KeyError:
            pass
except FileNotFoundError:
    login = classes.Login()
    login.mainloop()
