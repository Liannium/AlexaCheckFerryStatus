import requests
from vesselfunctions import getbiseattleferries, loadvessellist, loadterminallist

terminalurl = "https://www.wsdot.wa.gov/ferries/vesselwatch/Terminals.ashx"
vesselurl = "https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx"

vesselresp = requests.get(vesselurl)
terminalresp = requests.get(terminalurl)

if vesselresp.status_code == 200 and terminalresp.status_code == 200:
    vessellist = loadvessellist(vesselresp)
    terminallist = loadterminallist(terminalresp)

    route = input("Enter a route: ")
    if route == "SEA-BI":
        print(getbiseattleferries(vessellist, terminallist))

else:
    print("The page could not be successfully accessed")
