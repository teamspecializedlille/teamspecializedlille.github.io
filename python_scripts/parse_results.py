import requests
import re
import xlrd
import team_members
import race_results
import urllib3
import json


base = "https://cyclismeufolep5962.fr/"
column_name = 1
column_team = 2
column_result = 0
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ParseResults:
    
    race_date = ""
    race_name = ""
    race_type = ""
    race_year = ""
    race_cat = ""
    races_parsed = []
    team ={} 

    def __init__(self, team, results):
        self.team = team
        self.results = results
        self.race_date = ""
        self.race_name = ""
        self.race_type = ""
        self.race_year = ""
        self.races_parsed = []

    def display_race_infos(self):
        print("__________________________________________________________________________")
        print("Type: " + self.race_type + ", name: "+ self.race_name + ", date: "+ self.race_date+ "("+self.race_year+")")
        print("__________________________________________________________________________")

    def get_hash_race(self):
        return self.race_type + "/" + self.race_year + "/" + self.race_name

    def get_hash_individual_race(self):
        #year / race / cate /  => pos 
        return self.race_date + "|" + self.race_name + "|" + self.race_cat

    def parse_results_race_sheet(self, workbook, sheet):
        sheet = workbook.sheet_by_index(sheet)
        self.race_cat = sheet.name
        #print("Catégorie : " + self.race_cat)
        for line in range(sheet.nrows):
            
            if ("TEAM SPECIALIZED LILLE" in str(sheet.cell(line, column_team).value)):
                member = sheet.cell(line, column_name).value
                if (member not in self.team):
                    self.team[member] = team_members.TeamMember(member)
                self.team[member].course += 1
                hash_individual = self.get_hash_individual_race()
                if (self.race_type == "Cyclo Cross"):
                    self.team[member].cx[hash_individual] = sheet.cell(line, column_result).value
                elif (self.race_type == "VTT"):
                    self.team[member].vtt[hash_individual] = sheet.cell(line, column_result).value
                elif (self.race_type == "Route"):
                    self.team[member].road[hash_individual] = sheet.cell(line, column_result).value

                hash_race = self.get_hash_race()
                if (hash_race not in self.results):
                    self.results[hash_race] = race_results.RaceResults(hash_race)
                if (self.race_cat == "1ère"):
                    self.results[hash_race].one[member] = sheet.cell(line, column_result).value
                elif (self.race_cat == "2ème"):
                    self.results[hash_race].two[member] = sheet.cell(line, column_result).value
                elif (self.race_cat == "3ème"):
                    self.results[hash_race].three[member] = sheet.cell(line, column_result).value
                elif (self.race_cat == "Cadets"):
                    self.results[hash_race].cadet[member] = sheet.cell(line, column_result).value
                elif (self.race_cat == "Féminines"):
                    self.results[hash_race].fem[member] = sheet.cell(line, column_result).value

       

    def parse_results_race(self, file_url):
        #print(file_url)
        r = requests.get(file_url, verify=False)
        if (r.status_code == 200):
            output = open('test.xls', 'wb')
            output.write(r.content)

            workbook = xlrd.open_workbook('test.xls')
            self.parse_results_race_sheet( workbook, 0)
            self.parse_results_race_sheet( workbook, 1)
            self.parse_results_race_sheet( workbook, 2)
            self.parse_results_race_sheet( workbook, 3)
            self.parse_results_race_sheet( workbook, 4)
            return True
        else:
            return False

    def set_race_date(self,line):

        date = re.search(r"(.*)(\d\d\/\d\d\/\d\d\d\d)(.*)", line)
        if (date):
            date = re.search(r"(\d\d)\/(\d\d)\/(\d\d\d\d)", date.group(2))
            self.race_date = date.group(3) + "/" + date.group(2) + "/" + date.group(1)

    def set_race_infos(self, line):
        
        reg = re.search(r"(.*)\/(\d\d\d\d)\/(.*)\/(.*)", line)
        if (reg):
            self.race_name = reg.group(3)
            self.race_type = reg.group(1)
            self.race_year = reg.group(2)

    
    def load_races_parsed(self):
        races_parsed = []
        races_parsed_file = open("_data/races_parsed.json", 'r')
        data = json.load(races_parsed_file)
        if (len(data['races_parsed']) > 0):
            for race in data['races_parsed']:
                races_parsed.append(race)
        races_parsed_file.close()
        return races_parsed


    def save_races_parsed(self,races_parsed):
        data = {}
        data["races_parsed"] = races_parsed
        json_object = json.dumps(data,ensure_ascii=False)
        with open("data/races_parsed.json", "w", encoding='utf8') as outfile:
            outfile.write(json_object)
    
    def parse_race_payload(self, res):
        for line in res:
            
            if "/" in line:
                self.set_race_date(line)
            if "Classements.xls" in line:
                file = re.search(r"(.*)='(.*)'(.*)", line).group(2)
                self.set_race_infos(file)
                
                if (file not in  self.races_parsed):
                    url = base + file
                    if (self.parse_results_race(url)):
                        self.races_parsed.append(file)
                        self.display_race_infos()


    def generate_results(self):
        self.races_parsed = self.load_races_parsed()

        myobj = {'saison': '2024'}
        #cross
        r = requests.post('https://cyclismeufolep5962.fr/calResCross.php',verify=False,data=myobj ).text.splitlines()
        self.parse_race_payload(r)
        #vtt
        r = requests.post('https://cyclismeufolep5962.fr/calResVTT.php',verify=False,data=myobj ).text.splitlines()
        self.parse_race_payload(r)
        #road
        r = requests.post('https://cyclismeufolep5962.fr/calResRoute.php',verify=False,data=myobj ).text.splitlines()
        self.parse_race_payload(r)

        self.save_races_parsed(self.races_parsed)
        return self.team