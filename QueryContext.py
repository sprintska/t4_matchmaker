import json
import requests


HASURA_ENDPOINT_URL = "http://localhost:8080/v1/graphql"


def Query(operation_name, operation_doc, variables):

    url = HASURA_ENDPOINT_URL

    r = requests.post(
        url,
        json={
            "query": str(operation_doc),
            "variables": variables,
            "operationName": operation_name,
        },
    )

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
