from espn_api.football import League as Football_league
from espn_api.hockey import League as Hockey_league


def score_day_hockey(league, year, team) -> tuple:
    data = Hockey_league(league_id=league, year=year)
    # Team is in a list and index start 0
    team_id = team - 1
    # Get name of the team
    name = data.teams[team_id].team_name
    # Get scores data of the league
    box_scores = data.box_scores(data.current_week)
    str_box_scores = []
    index = int()

    for i in box_scores:
        # Box_scores in espn class, so I change in to str to find the good matchup
        str_box_scores.append(str(i))
    for i in str_box_scores:
        # Get the index of my team matchup
        if i.find(name) > 0:
            index = str_box_scores.index(i)

    # Finaly get the matchup score and team and return it
    home_s = box_scores[index].home_score
    away_s = box_scores[index].away_score
    home_t = box_scores[index].home_team
    away_t = box_scores[index].away_team

    return home_t, home_s, away_t, away_s


# Same function but for football
def score_day_football(league, year, team) -> tuple:
    data = Football_league(league_id=league, year=year)
    team_id = team - 1
    name = data.teams[team_id].team_name
    box_scores = data.box_scores(data.current_week)
    str_box_scores = []
    index = int()

    for i in box_scores:
        str_box_scores.append(str(i))
    for i in str_box_scores:
        if i.find(name) > 0:
            index = str_box_scores.index(i)

    home_s = box_scores[index].home_score
    away_s = box_scores[index].away_score
    home_t = box_scores[index].home_team
    away_t = box_scores[index].away_team

    return home_t, home_s, away_t, away_s
