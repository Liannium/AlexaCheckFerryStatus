import requests
from vesselfunctions import getseattleferries, loadvessellist, loadterminallist, getEdKingferries, getSeaBrferries

vessellist = loadvessellist()
terminallist = loadterminallist()

if terminallist is not None and vessellist is not None:
    route = input("Enter a route: ")
    if route == "SEA-BI":
        print(getseattleferries(vessellist, terminallist, "SEA-BI", "Bainbridge Island"))
    if route == "ED-KING":
        print(getEdKingferries(vessellist, terminallist))
    if route == "SEA-BR":
        print(getSeaBrferries(vessellist, terminallist))
else:
    print("The page could not be successfully accessed")
