import requests
from flask import current_app as app


def Query(operation_name, operation_doc, variables):

    url = "https://{}".format(app.config["HASURA_URL"])
    data = {
        "query": str(operation_doc),
        "variables": variables,
        "operationName": operation_name,
    }
    headers = {"X-Hasura-Admin-Secret": app.config["HASURA_ADMIN_SECRET"]}

    r = requests.post(url, json=data, headers=headers)

    return r.json()


def getMatchHistory(tourney_id):

    operation_name = "getMatchHistory"
    vars = {"tournament_id": str(tourney_id)}
    get_match_history_doc = """
        query getMatchHistory($tournament_id: uuid = "") {
            Match(where: {tournament_id: {_eq: $tournament_id}}) {
                Players {
                    player_id
                }
            }
            Tournament(where: {id: {_eq: $tournament_id}}) {
                Ladder {
                    id
                    tournament_points
                    mov
                    sos
                }
            }
        }
    """

    match_history = Query(operation_name, get_match_history_doc, vars)

    return match_history
