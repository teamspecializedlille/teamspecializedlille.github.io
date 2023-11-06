import requests
import re
import xlrd
import team_members
import race_results
import urllib3
import json


base = "https://cyclismeufolep5962.fr/"
column_result = 0
column_name = 1
column_team = 2
column_lap = 3
column_time = 4
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
        self.scratch = {}

    def display_race_infos(self):
        print("__________________________________________________________________________")
        print("Type: " + self.race_type + ", name: "+ self.race_name + ", date: "+ self.race_date+ "("+self.race_year+")")
        print("__________________________________________________________________________")

    def get_hash_race(self):
        return self.race_type + "/" + self.race_year + "/" + self.race_name

    def get_hash_individual_race(self):
        #year / race / cate /  => pos 
        return self.race_date + "|" + self.race_name + "|" + self.race_cat

    def return_result(self, sheet, line):
        val = sheet.cell(line, column_result).value
        if (val == "Ab" or val == "AB" or val == ""):
            return val
        return int(val)

    def is_team_member(self, sheet, line):
        if (line <= 1 ):
            return False
        if ("TEAM SPECIALIZED LILLE" in str(sheet.cell(line, column_team).value)):
            return True
        
        elif ( str(sheet.cell(line, column_team).value) == ""  ):

            if (sheet.cell(line, column_result).value == "Ab" or sheet.cell(line, column_result).value == "AB"):
                member = sheet.cell(line, column_name).value
                if member in self.team:
                    return True
        return False

    def parse_results_race_sheet(self, workbook, sheet):
        sheet = workbook.sheet_by_index(sheet)
        self.race_cat = sheet.name
        hash_race = self.get_hash_race()
        print(hash_race)
        if (hash_race not in self.results):
            self.results[hash_race] = race_results.RaceResults(hash_race)
        for line in range(sheet.nrows):
            if (str(sheet.cell(line, column_team).value) != ""):
                if (self.race_cat == "1ère"):
                    self.results[hash_race].one_riders += 1
                elif (self.race_cat == "2ème"):
                    self.results[hash_race].two_riders += 1
                elif (self.race_cat == "3ème"):
                    self.results[hash_race].three_riders += 1
                elif (self.race_cat == "Cadets"):
                    self.results[hash_race].cadet_riders += 1
                elif (self.race_cat == "Féminines"):
                   self.results[hash_race].fem_riders += 1
                elif (self.race_cat == "Séniors A"):
                    self.results[hash_race].VTTSeniorsA_riders += 1
                elif (self.race_cat == "Seniors B"):
                    self.results[hash_race].VTTSeniorsB_riders += 1
                elif (self.race_cat == "Vétérans A"):
                    self.results[hash_race].VTTVeteransA_riders += 1
                elif (self.race_cat == "Vétérans B"):
                    self.results[hash_race].VTTVeteransB_riders += 1
                elif (self.race_cat == "Vétérans C"):
                    self.results[hash_race].VTTVeteransC_riders += 1
            if (self.is_team_member(sheet, line)):
                member = sheet.cell(line, column_name).value
                if (member not in self.team):
                    self.team[member] = team_members.TeamMember(member)
                self.team[member].course += 1
                hash_individual = self.get_hash_individual_race()
                if (self.race_type == "Cyclo Cross"):
                    self.team[member].cx[hash_individual] = self.return_result(sheet,line)
                elif (self.race_type == "VTT"):
                    self.team[member].vtt[hash_individual] = self.return_result(sheet,line)
                elif (self.race_type == "Route"):
                    self.team[member].road[hash_individual] = self.return_result(sheet,line)
                if (self.race_cat == "1ère"):
                    self.results[hash_race].one[member] = self.return_result(sheet,line)
                elif (self.race_cat == "2ème"):
                    self.results[hash_race].two[member] = self.return_result(sheet,line)
                elif (self.race_cat == "3ème"):
                    self.results[hash_race].three[member] = self.return_result(sheet,line)
                elif (self.race_cat == "Cadets"):
                    self.results[hash_race].cadet[member] = self.return_result(sheet,line)
                elif (self.race_cat == "Féminines"):
                    self.results[hash_race].fem[member] = self.return_result(sheet,line)
                elif (self.race_cat == "Seniors A"):
                    self.results[hash_race].VTTSeniorsA[member] = self.return_result(sheet,line)
                elif (self.race_cat == "Seniors B"):
                    self.results[hash_race].VTTSeniorsB[member] = self.return_result(sheet,line)
                elif (self.race_cat == "Vétérans A"):
                    self.results[hash_race].VTTVeteransA[member] = self.return_result(sheet,line)
                elif (self.race_cat == "Vétérans B"):
                    self.results[hash_race].VTTVeteransB[member] = self.return_result(sheet,line)
                elif (self.race_cat == "Vétérans C"):
                    self.results[hash_race].VTTVeteransC[member] = self.return_result(sheet,line)
            member = sheet.cell(line, column_name).value
            if (member != "" and line > 1):
                print("|"+str(sheet.cell(line, column_time).value)+"|")
                if (sheet.cell(line, column_time).value == ""):
                    test = (40, 0, 0, 0, 38, 53)
                else:
                    test = xlrd.xldate.xldate_as_tuple(sheet.cell(line, column_time).value, sheet.book.datemode)
                lap =  sheet.cell_value(line, column_lap)
                if (lap == ""):
                    lap = 0
                self.scratch[member] = {"team": sheet.cell_value(line, column_team), "lap": lap, "time" : test, "cat": self.race_cat}

    def get_relevant_skills(self, item):
        """Get the sum of Python and JavaScript skill"""
        print("jhdkjezhdjzhe")
        print(item)
        time = item[1].get("time", 0)[3]*60*60+item[1].get("time", 0)[4]*60+item[1].get("time", 0)[5]
        res =  item[1].get("lap", 0) + time
        print(res)
        return (item[1].get("lap", 0)*-1 ,  time)
        return res
        # Return default value that is equivalent to no skill
        return skills.get("python", 0) + skills.get("js", 0)


    def parse_results_race(self, file_url):
        r = requests.get(file_url, verify=False)
        if (r.status_code == 200):
            output = open('test.xls', 'wb')
            output.write(r.content)            
            
            self.scratch = {}
            workbook = xlrd.open_workbook('test.xls')
            self.parse_results_race_sheet( workbook, 0)
            self.parse_results_race_sheet( workbook, 1)
            self.parse_results_race_sheet( workbook, 2)
            self.parse_results_race_sheet( workbook, 3)
            self.parse_results_race_sheet( workbook, 4)
            print(self.scratch)

            sorted_list = sorted(self.scratch.items(), key=self.get_relevant_skills, reverse=False)
            print("prepare")
            for res in sorted_list:
                print(res[1])
                print(res[1].get("time"))
                res[1]["time"] = (str(res[1]["time"][3]) +":"+str(res[1]["time"][4])+":" +str(res[1]["time"][5]) )

            data = {}
            data["scratch"] = sorted_list
            json_object = json.dumps(data,ensure_ascii=False)
            with open("../_data/test.json", "w", encoding='utf8') as outfile:
                outfile.write(json_object)

            exit(0)
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
        races_parsed_file = open("../_data/races_parsed.json", 'r')
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
        with open("../_data/races_parsed.json", "w", encoding='utf8') as outfile:
            outfile.write(json_object)
    
    def create_post_race(self):
        hash =  self.get_hash_race()
        if (len(self.results) == 0 ):
            return
        if (len(self.results[ hash].one.keys()) == 0 and len(self.results[ hash].two.keys())==0 and len(self.results[ hash].three.keys()) ==0  and len(self.results[ hash].fem.keys()) == 0  
            and len(self.results[ hash].cadet.keys())==0  and len(self.results[ hash].VTTSeniorsA.keys())==0  and len(self.results[ hash].VTTSeniorsB.keys())==0  and len(self.results[ hash].VTTVeteransA.keys())==0  
            and len(self.results[ hash].VTTVeteransB.keys())==0 and len(self.results[ hash].VTTVeteransC.keys())==0  ):
            return
        file_name = self.race_date.replace("/", "-") + "-" + self.race_type.replace(" ", "") + self.race_name.replace(" ", "-") + ".md"
        with open("../_posts/" + file_name, "w", encoding='utf8') as outfile:
            outfile.write("---\n")
            outfile.write("layout: post\n")
            outfile.write("title: " + self.race_type + " - " + self.race_name + " - " + self.race_year + "\n")
            outfile.write("date: " + self.race_date.replace("/", "-") + "\n")
            outfile.write("category: " + self.race_type + "\n")
            outfile.write("tags: " + self.race_type + "\n")
            if (self.race_type == "Cyclo Cross"):
                outfile.write("image: assets/img/blog/cx.jpeg\n")
            elif (self.race_type == "VTT"):
                outfile.write("image: assets/img/blog/vtt.jpeg\n")
            elif (self.race_type == "Route"):
                outfile.write("image: assets/img/blog/road.jpeg\n")
            outfile.write("---\n")
           
            result_to_display =  self.results[hash].one
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### 1ère Catégorie\n")
                outfile.write( str(self.results[hash].one_riders )+ " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

            
            result_to_display =  self.results[ hash].two
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### 2ème Catégorie\n")
                outfile.write( str(self.results[hash].two_riders) + " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

            
            result_to_display =  self.results[ hash].three
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### 3ème Catégorie\n")
                outfile.write( str(self.results[hash].three_riders) + " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

            result_to_display =  self.results[ hash].fem
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### Féminines\n")
                outfile.write( str(self.results[hash].fem_riders) + " participantes\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

           
            result_to_display =  self.results[ hash].cadet
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### Cadets\n")
                outfile.write( str(self.results[hash].cadet_riders) + " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

            result_to_display =  self.results[ hash].VTTSeniorsA
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### VTT Sénior A\n")
                outfile.write( str(self.results[hash].VTTSeniorsA_riders) + " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

            result_to_display =  self.results[ hash].VTTSeniorsB
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### VTT Sénior B\n")
                outfile.write( str(self.results[hash].VTTSeniorsB_riders) + " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

            result_to_display =  self.results[ hash].VTTVeteransA
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### VTT Vétérans A\n")
                outfile.write( str(self.results[hash].VTTVeteransA_riders) + " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

            result_to_display =  self.results[ hash].VTTVeteransB
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### VTT Vétérans B\n")
                outfile.write( str(self.results[hash].VTTVeteransB_riders) + " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")

            result_to_display =  self.results[ hash].VTTVeteransC
            if (len(result_to_display.keys()) > 0):
                outfile.write("\n### VTT Vétérans C\n")
                outfile.write( str(self.results[hash].VTTVeteransC_riders) + " participants\n")
            for line in result_to_display.keys():
                outfile.write("- " + line + " : " + str(result_to_display[line]) + "\n")
            self.results = {}

    def parse_race_payload(self, res):
        for line in res:
            
            if "/" in line:
                self.set_race_date(line)
            if "Classements.xls" in line:
                file = re.search(r"(.*)='(.*)'(.*)", line).group(2)
                self.set_race_infos(file)
                
                if (file not in  self.races_parsed or True):
                    url = base + file
                    if (self.parse_results_race(url)):
                        self.races_parsed.append(file)
                        self.display_race_infos()
                        print(self.results)
                        self.create_post_race()


    def generate_results(self):
        self.races_parsed = self.load_races_parsed()

        x = range(2023, 2024)

        for n in x:
            myobj = {'saison': str(n)}
            

      
        
            #myobj = {'saison': str(2024)}

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
