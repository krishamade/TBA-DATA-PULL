import requests
import tkinter as tk
from tkinter import simpledialog
import pypyodbc as db

#Below is the SQL Database Information
#Enter the MSSQL Servername and the Instance
servername = "localhost\SQLEXPRESS"
#Enter the Database Name
database = "{INSERT DATABASE NAME}"
#Enter the MSSQL Username
username = "{INSERT MSSQL USERNAME}"
#Enter the MSSQL Password
password = "{MSSQL DATABASE PASSWORD}"

cnn = db.connect("Driver={SQL Server Native Client 11.0};"
                      f"Server={servername};"
                      f"Database={database};"
                      f"UID={username};"
                      f"PWD={password};"
                      "Trusted_Connection=yes;")

application_window = tk.Tk()

key = 'X-TBA-Auth-Key'
authkey = '{INSERT THE BLUE ALLIANCE API KEY HERE}'

#tbaYear = simpledialog.askstring("Year", "What is year is the event in? ", parent=application_window)

#tbaState = simpledialog.askstring("Year", "What is state is the event in? ", parent=application_window)

#tbaEvent = simpledialog.askstring("Event ID", "What is the event ID? ", parent=application_window)

#Variables for testing purposes. Remove in production in place of user inputs or dropdowns

#Replace With Event ID
tbaEvent = "2019mimil"

tbaYear = "2019"
tbaState = "MI"

eventRequest = requests.get(f"https://www.thebluealliance.com/api/v3/events/{tbaYear}/simple", headers={key: authkey})

matchRequest = requests.get(f"https://www.thebluealliance.com/api/v3/event/{tbaEvent}/matches/simple", headers={key: authkey})

matchResults = matchRequest.json()
eventResults = eventRequest.json()

for t in eventResults:
    if t['state_prov'] == f'{tbaState}':
        print(t['name'] + " " + t['key'])

if matchResults is []:
    print(f"There is not match data available for {tbaEvent} at this time")

cursor = cnn.cursor()

for x in matchResults:
    time = x['actual_time']
    matches = x['match_number']
    compLevels = x['comp_level']
    blueAlliance = x['alliances']['blue']['team_keys']
    redAlliance = x['alliances']['red']['team_keys']

    blueRobot1 = blueAlliance[0]
    blueRobot2 = blueAlliance[1]
    blueRobot3 = blueAlliance[2]
    redRobot1 = redAlliance[0]
    redRobot2 = redAlliance[1]
    redRobot3 = redAlliance[2]

    cursor.execute("INSERT INTO TBAMatchData(match_number, comp_level, event_id, actual_time, blue_alliance_robot_1, blue_alliance_robot_2, blue_alliance_robot_3, red_alliance_robot_1, red_alliance_robot_2, red_alliance_robot_3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (matches, compLevels, tbaEvent, time, blueRobot1, blueRobot2, blueRobot3, redRobot1, redRobot2, redRobot3))
    print(f'{matches} {compLevels} {blueAlliance} {redAlliance}')

cnn.commit()
