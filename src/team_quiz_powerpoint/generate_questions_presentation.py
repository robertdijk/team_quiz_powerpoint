import argparse
from pathlib import Path

import collections
import collections.abc
from pptx import Presentation

from team_quiz_powerpoint.config_parser import load_config
from team_quiz_powerpoint.pickeling import load_quiz
from team_quiz_powerpoint.slides import question_slide, rules_slide, title_slide, qr_slide


def main():
    parser = argparse.ArgumentParser(description='Make question presentation from quiz')
    parser.add_argument('-c', '--config', default=None, help="config file")
    args = parser.parse_args()

    config = load_config(args.config)

    quiz = load_quiz(config["pickle-file"])

    prs = Presentation(config["template-file"])

    if config["title"]:
        title_slide(prs, config["title"], music=False)

    if config["question-presentation"]["rules-slide"]:
        rules_slide(prs, config["question-presentation"]["rules-slide"]["rules"],
                    config["question-presentation"]["rules-slide"]["title"])

    if config["question-presentation"]["qr-slide"]:
        qr_slide(prs, config["question-presentation"]["qr-slide"]["url"],
                 config["question-presentation"]["qr-slide"]["title"])

    for i, q in enumerate(quiz.questions):
        question_slide(prs, q, i, config["question-presentation"]["timer"], config["question-presentation"]["music"])

    if config["question-presentation"]["end-title"]:
        title_slide(prs, config["question-presentation"]["end-title"])

    prs.save(config["question-presentation"]["file"])


if __name__ == '__main__':
    main()
