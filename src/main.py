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


@app.command()
def exploits(vulnerability_id: str, format_cli: bool = True):
    exploits = get_exploits(vulnerability_id)
    if(format_cli):
        format_report_table(exploits, vulnerability_id)
    else:
        print(json.dumps(exploits))

def get_exploits(vulnerability_id: str):
    return __get_exploit_reports(vulnerability_id, "exploit")

def get_exploitations(vulnerability_id: str):
    return __get_exploit_reports(vulnerability_id, "exploitation")

def __get_exploit_reports(vulnerability_id: str, type: str):
    exploits = []
    for row in cur.execute('SELECT id, referenceURL, timeStamp FROM exploits WHERE type=? AND id=?', [type, vulnerability_id]):
        exploit = collections.OrderedDict()
        exploit['id'] = row[0]
        exploit['referenceURL'] = row[1]
        exploit['timeStamp'] = row[2]
        exploits.append(exploit)
    return exploits


@app.command()
def reports(vulnerability_id: str, format_cli: bool = True):
    report = get_report(vulnerability_id)
    if(format_cli):
        format_full_report_table(report)
    else:
        print(json.dumps(report))


def get_report(vulnerability_id: str):
    details = get_vulnerability_description(vulnerability_id)
    return { "id": details["id"], "description": details["description"], "exploitations": get_exploitations(vulnerability_id), "exploits": get_exploits(vulnerability_id)}


def get_vulnerability_description(vulnerability_id: str):
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
    for exploitation in output["exploitations"]:
        formatted.append(
            ["", "", exploitation["referenceURL"], exploitation["timeStamp"]])
    if(len(output["exploitations"]) == 0):
        formatted.append(["", "", "No reports of exploitation inTheWild", ""])
    for exploit in output["exploits"]:
        formatted.append(
            ["", "", exploit["referenceURL"], exploit["timeStamp"]])
    if(len(output["exploits"]) == 0):
        formatted.append(["", "", "No reports of exploits available", ""])
    formatted[1][0] = output["id"]
    formatted[2][0] = output["description"]
    formatted[1][1] = "exploitation"
    if(len(output["exploitations"]) == 0):
        formatted[len(output["exploitations"])+2][1] = "exploit"
    else:
        formatted[len(output["exploitations"])+1][1] = "exploit"
    table = Texttable(max_width=150)
    table.add_rows(formatted)
    print(table.draw())


if __name__ == "__main__":
    app()
