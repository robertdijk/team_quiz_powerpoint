import os
import typing
from pathlib import Path

import tomli
from schema import Schema, Optional, Use, And

SCHEMA = Schema({
    Optional("title", default="Quiz"): str,
    Optional("pickle-file", default="quiz.pickle"): Use(Path),
    "import": {
        "questions": {
            "fields": {
                Optional("name-field", default="Name"): str,
                Optional("team-field", default="Team"): str,
                Optional("question-field", default="Question"): str,
                Optional("correct-answer-field", default="Correct answer"): str,
                Optional("wrong-answer-field-1", default="Wrong answer 1"): str,
                Optional("wrong-answer-field-2", default="Wrong answer 2"): str,
                Optional("wrong-answer-field-3", default="Wrong answer 3"): str,
            }
        },
        "answers": {
            "fields": {
                Optional("name-field", default="Name"): str,
                Optional("team-field", default="Team"): str,
                Optional("question-field", default="Question {}"): str,
            }
        }
    },
    Optional("template-file", default="template.pptx"): And(os.path.exists, Use(Path)),
    "question-presentation": {
        Optional("file", default="questions.pptx"): Use(Path),
        Optional("timer", default=True): bool,
        Optional("music", default=True): bool,
        Optional("end-title", default="End"): str,
        Optional("rules-slide"): {
            Optional("title", default="Rules"): str,
            "rules": [str],
        },
        Optional("qr-slide"): {
            Optional("title", default="Scan the QR-code"): str,
            "url": str,
        },
    },
    "solution-presentation": {
        Optional("file", default="solutions.pptx"): Use(Path),
        Optional("music", default=True): bool,
        Optional("podium-slide", default=True): bool,
        Optional("team-slide", default=True): bool,
    }
})


def load_config(file: typing.Optional[Path] = None):
    if not file:
        file = Path("config.toml")

    if file.is_file():
        with open(file, mode="rb") as fp:
            config = tomli.load(fp)
    else:
        config = {}

    config = SCHEMA.validate(config)
    return config
