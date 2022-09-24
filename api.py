from NextRoundMatchesTypes import NextRoundMatchesArgs, NextRoundMatchesOutput
from flask import Flask, request, jsonify
from matchmaker import Matchmaker

app = Flask(__name__)


@app.route("/NextRoundMatches", methods=["POST"])
def NextRoundMatchesHandler():
    args = NextRoundMatchesArgs.from_request(request.get_json())
    mm = Matchmaker(args.tournament_id)
    mm.generateMatches()

    [print(p) for p in mm.pairings]

    return NextRoundMatchesOutput(mm.pairings).to_json()


if __name__ == "__main__":
    print("I was run-ningh!")
    app.run(debug=True, host="0.0.0.0")
