from vesselfunctions import getseattleferries, loadvessellist, loadterminallist, checkferries, checkFVSferries

vessellist = loadvessellist()
terminallist = loadterminallist()

if terminallist is not None and vessellist is not None:
    route = input("Enter a route: ")
    if route == "SEA-BI":
        print(getseattleferries(vessellist, terminallist, "SEA-BI", "Bainbridge Island"))
    if route == "ED-KING":
        print(checkferries(vessellist, terminallist, "ED-KING", "Edmonds", "Kingston"))
    if route == "SEA-BR":
        print(getseattleferries(vessellist, terminallist, "SEA-BR", "Bremerton"))
    if route == "MUK-CL":
        print(checkferries(vessellist, terminallist, "MUK-CL", "Mukilteo", "Clinton"))
    if route == "PD-TAL":
        print(checkferries(vessellist, terminallist, "PD-TAL", "Point Defiance", "Tahlequah"))
    if route == "F-V-S":
        print(checkFVSferries(vessellist, terminallist))
else:
    print("The page could not be successfully accessed")
