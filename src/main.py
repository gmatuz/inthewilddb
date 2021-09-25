import typer
import json
import collections
from texttable import Texttable
import sqlite3
con = sqlite3.connect('inthewild.db')
cur = con.cursor()

app = typer.Typer()


@app.command()
def exploitations(vulnerability_id: str, format_cli: bool = True):
    exploitations = get_exploitations(vulnerability_id)
    if(format_cli):
        format_report_table(exploitations, vulnerability_id)
    else:
        print(json.dumps(exploitations))


def get_exploitations(vulnerability_id: str):
    exploitations = []
    for row in cur.execute('SELECT id, referenceURL as url, timeStamp FROM exploits WHERE type="exploitation" AND id=?', [vulnerability_id]):
        exploitation = collections.OrderedDict()
        exploitation['id'] = row[0]
        exploitation['referenceURL'] = row[1]
        exploitation['timeStamp'] = row[2]
        exploitations.append(exploitation)
    return exploitations


@app.command()
def exploits(vulnerability_id: str, format_cli: bool = True):
    exploits = get_exploits(vulnerability_id)
    if(format_cli):
        format_report_table(exploits, vulnerability_id)
    else:
        print(json.dumps(exploits))


def get_exploits(vulnerability_id: str):
    exploits = []
    for row in cur.execute('SELECT id, referenceURL, timeStamp FROM exploits WHERE type="exploit" AND id=?', [vulnerability_id]):
        exploit = collections.OrderedDict()
        exploit['id'] = row[0]
        exploit['referenceURL'] = row[1]
        exploit['timeStamp'] = row[2]
        exploits.append(exploit)
    return exploits


@app.command()
def reports(vulnerability_id: str, format_cli: bool = True):
    report = get_reports(vulnerability_id)
    if(format_cli):
        format_full_report_table(report)
    else:
        print(json.dumps(report))


def get_reports(vulnerability_id: str):
    return {"background": get_vulnerability_details(vulnerability_id), "exploitation": get_exploitations(vulnerability_id), "exploit": get_exploits(vulnerability_id)}


def get_vulnerability_details(vulnerability_id: str):
    cur.execute('SELECT id, description FROM vulns WHERE id=?',
                [vulnerability_id])
    vulnerability = cur.fetchone()
    if(vulnerability == None):
        return {"id": vulnerability_id, "description": "Vulnerability description missing"}
    return {"id": vulnerability[0], "description": vulnerability[1]}


def format_report_table(reports, vulnerability_id):
    formatted = []
    formatted.append(["Vulnerability", "URL", "Report Time"])
    for exploitation in reports:
        formatted.append(["", exploitation["referenceURL"],
                         exploitation["timeStamp"]])
    if(len(reports) == 0):
        formatted.append(["", "No reports", ""])
    formatted[1][0] = vulnerability_id
    table = Texttable(max_width=100)
    table.add_rows(formatted)
    print(table.draw())


def format_full_report_table(output):
    formatted = []
    formatted.append(["Vulnerability", "report", "URL", "Report Time"])
    for exploitation in output["exploitation"]:
        formatted.append(
            ["", "", exploitation["referenceURL"], exploitation["timeStamp"]])
    if(len(output["exploitation"]) == 0):
        formatted.append(["", "", "No reports of exploitation inTheWild", ""])
    for exploit in output["exploit"]:
        formatted.append(
            ["", "", exploit["referenceURL"], exploit["timeStamp"]])
    if(len(output["exploit"]) == 0):
        formatted.append(["", "", "No reports of exploits available", ""])
    formatted[1][0] = output["background"]["id"]
    formatted[2][0] = output["background"]["description"]
    formatted[1][1] = "exploitation"
    if(len(output["exploitation"]) == 0):
        formatted[len(output["exploitation"])+2][1] = "exploit"
    else:
        formatted[len(output["exploitation"])+1][1] = "exploit"
    table = Texttable(max_width=150)
    table.add_rows(formatted)
    print(table.draw())


if __name__ == "__main__":
    app()
