import json
import team_members

team_path_file = '../_data/team.json'

class TeamMember:
    def __init__(self,name):
        self.name = name
        self.course = 0
        self.cx = {}
        self.vtt = {}
        self.road = {}


    def to_dict(self):
        res = {}
        res["name"] = self.name
        res["course"] = self.course
        res["cx"] =  dict(sorted(self.cx.items(), reverse=True))
        res["vtt"] = dict(sorted(self.vtt.items(), reverse=True))
        res["road"] = dict(sorted(self.road.items(), reverse=True))
        return res

def load_team_from_file(team: dict[str, TeamMember]) -> dict[str, TeamMember]:
    team_file = open(team_path_file, 'r')
    data = json.load(team_file)
 
    for member in data['team_members']:
        team[member["name"]] = TeamMember(member["name"])
        team[member["name"]].course = member["course"]
        team[member["name"]].cx = member["cx"]
        team[member["name"]].vtt = member["vtt"]
        team[member["name"]].road = member["road"]
       

 
    team_file.close()
    return team

def remove_old_team(team):
    if ("BOONE ERIC" in team):
        team.pop("BOONE ERIC")
    if ("BRADEFER GERY" in team):
        team.pop("BRADEFER GERY")
    if ("DEBUY SEBASTIEN" in team):
        team.pop("DEBUY SEBASTIEN")
    if ("DARQUE JEAN FRANCOIS" in team):
        team.pop("DARQUE JEAN FRANCOIS")
    if ("DUFOUR JONATHAN" in team):
        team.pop("DUFOUR JONATHAN")
    if ("VERHULST ERIC" in team):
        team.pop("VERHULST ERIC")

def update_team_file(team):
    data = {}
    array = []
    remove_old_team(team)
    for m in team.values():
        array.append(m.to_dict())
    data["team_members"] = array
    json_object = json.dumps(data,ensure_ascii=False)
    with open(team_path_file, "w", encoding='utf8') as outfile:
        outfile.write(json_object)
   