import os
import requests


def Query(operation_name, operation_doc, variables):

    url = "https://{}/v1/graphql".format(os.environ.get("MATCHMAKER_HASURA_URL"))
    data = {
        "query": str(operation_doc),
        "variables": variables,
        "operationName": operation_name,
    }

    headers = {
        "X-Hasura-Admin-Secret": os.environ.get("MATCHMAKER_HASURA_ADMIN_SECRET")
    }

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
                round
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


def createMatches(tourney_id, round, count):

    operation_name = "CreateMatches"
    vars = [{"tournament_id": tourney_id, "round": round} for _ in range(count)]
    create_matches_doc = """
        mutation CreateMatches($matches: [Match_insert_input!] !) {
        insert_Match(objects: $matches) {
            returning {
            id
            }
        }
        }
    """

    new_match_ids = Query(operation_name, create_matches_doc, vars)

    return new_match_ids
