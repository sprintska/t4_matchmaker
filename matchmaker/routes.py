from .NextRoundMatchesTypes import NextRoundMatchesArgs, NextRoundMatchesOutput
from .matchmaker import Matchmaker
from flask import request, current_app as app


@app.route("/NextRoundMatches", methods=["POST"])
def NextRoundMatchesHandler():
    args = NextRoundMatchesArgs.from_request(request.get_json())
    mm = Matchmaker(args.tournament_id)
    mm.generateMatches()

    [print(p) for p in mm.pairings]

    return NextRoundMatchesOutput(mm.pairings).to_json()
