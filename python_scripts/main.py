import team_members
import parse_results
import race_results

team = {}
results = {}

item = {'team': 'U.C. CAPELLOISE FOURMIES', 'lap': 7.0, 'time': (0, 0, 0, 1, 29, 12), 'cat': 'Féminines'}


team = team_members.load_team_from_file(team)


parser = parse_results.ParseResults(team, results)
team = parser.generate_results()
team_members.update_team_file(team)
