import team_members
import parse_results
import race_results

team = {}
results = {}


team = team_members.load_team_from_file(team)


parser = parse_results.ParseResults(team, results)
team = parser.generate_results()
print(team)
team_members.update_team_file(team)