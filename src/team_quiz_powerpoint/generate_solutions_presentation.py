import argparse

import collections
import collections.abc
from pptx import Presentation

from team_quiz_powerpoint.config_parser import load_config
from team_quiz_powerpoint.pickeling import load_quiz
from team_quiz_powerpoint.slides import answer_slide, podium_slide, teams_slide, teams_winning_slide, title_slide


def main():
    parser = argparse.ArgumentParser(description='Make solution presentation from quiz')
    parser.add_argument('-c', '--config', default=None, help="config file")
    args = parser.parse_args()

    config = load_config(args.config)

    quiz = load_quiz(config["pickle-file"])

    prs = Presentation(config["template-file"])

    if config["title"]:
        title_slide(prs, config["title"], music=config["solution-presentation"]["music"])

    for i in range(len(quiz.questions)):
        answer_slide(prs, quiz, i, False)
        answer_slide(prs, quiz, i, True)

    ranking = quiz.get_players_ranking()

    if config["solution-presentation"]["podium-slide"]:
        podium_slide(prs)
        podium_slide(prs, player3=ranking[2] if 2 < len(ranking) else None)
        podium_slide(prs, player2=ranking[1] if 1 < len(ranking) else None,
                     player3=ranking[2] if 2 < len(ranking) else None)
        podium_slide(prs, player1=ranking[0] if 0 < len(ranking) else None,
                     player2=ranking[1] if 1 < len(ranking) else None,
                     player3=ranking[2] if 2 < len(ranking) else None)

    if config["solution-presentation"]["team-slide"]:
        teams_slide(prs, quiz)
        teams_winning_slide(prs, quiz)

    prs.save(config["solution-presentation"]["file"])


if __name__ == '__main__':
    main()
