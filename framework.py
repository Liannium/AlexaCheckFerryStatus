import requests
import json
import re
from vesselfunctions import getbiseattleferries

terminalurl = "https://www.wsdot.wa.gov/ferries/vesselwatch/Terminals.ashx"
vesselurl = "https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx"

vesselresp = requests.get(vesselurl)
terminalresp = requests.get(terminalurl)

if vesselresp.status_code == 200 and terminalresp.status_code == 200:
    print("Successfully accessed pages!")
    vessels = json.loads(vesselresp.text)
    vessellist = vessels["vessellist"]

    regex = r'new Date\(\d*\)'
    terminalstring = re.sub(regex, "null", terminalresp.text, flags=re.MULTILINE)
    terminals = json.loads(terminalstring)
    terminallist = terminals["FeedContentList"]

    print(getbiseattleferries(vessellist, terminallist))
else:
    print("The page could not be successfully accessed")
