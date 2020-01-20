import requests
from vesselfunctions import getbiseattleferries, loadvessellist, loadterminallist, getEdKingferries, getSeaBrferries

vessellist = loadvessellist()
terminallist = loadterminallist()

if terminallist is not None and vessellist is not None:
    route = input("Enter a route: ")
    if route == "SEA-BI":
        print(getbiseattleferries(vessellist, terminallist))
    if route == "ED-KING":
        print(getEdKingferries(vessellist, terminallist))
    if route == "SEA-BR":
        print(getSeaBrferries(vessellist, terminallist))
else:
    print("The page could not be successfully accessed")
