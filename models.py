# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "a2wsgi>=1.10.10",
#     "bootstrap-flask>=2.5.0",
#     "curies>=0.12.9",
#     "flask>=3.1.2",
#     "pydantic>=2.12.5",
#     "uvicorn>=0.40.0",
# ]
# ///

from typing import Literal

from pydantic import BaseModel
from pathlib import Path
from curies import Reference
import flask
from flask_bootstrap import Bootstrap5
import uvicorn
from a2wsgi import WSGIMiddleware

HERE = Path(__file__).parent.resolve()
REACTIONS_PATH = HERE.joinpath("database.json")


class ReactionPart(BaseModel):
    reference: Reference
    state: Literal["soluble", "insoluble", "gas"]
    stoichiometry: int


class Reaction(BaseModel):
    inputs: list[ReactionPart]
    outputs: list[ReactionPart]
    solvent: Reference


class Database(BaseModel):
    reactions: list[Reaction]


database = Database.model_validate_json(REACTIONS_PATH.read_text())

app = flask.Flask(__name__)
Bootstrap5(app)


@app.route("/")
def home() -> str:
    return flask.render_template("index.html", database=database)


if __name__ == "__main__":
    uvicorn.run(WSGIMiddleware(app), host="0.0.0.0", port=8000)
