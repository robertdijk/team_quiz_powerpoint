import argparse
import logging
import random
from pathlib import Path
from typing import List

import pandas as pd

from team_quiz_powerpoint.config_parser import load_config
from team_quiz_powerpoint.helpers import load_excel_file
from team_quiz_powerpoint.pickeling import save_quiz, load_quiz
from team_quiz_powerpoint.model import Quiz

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel('DEBUG')


def main():
    parser = argparse.ArgumentParser(description='Import questions from excel file')
    parser.add_argument('excelfile')
    parser.add_argument('-c', '--config', default=None, help="config file")
    parser.add_argument('-m', '--max', type=int,
                        help="Maximum amount of questions. When specified it will randomly pick MAX questions")
    args = parser.parse_args()

    config = load_config(args.config)

    q = Quiz()

    df = load_excel_file(Path(args.excelfile))
    df.columns = [title.rstrip() for title in df.columns]

    for index, row in df.iterrows():
        q.add_question_from_row(row, config["import"]["questions"]["fields"])

    logger.info(f"Imported {len(q.questions)} question{'s' if (len(q.questions) != 1) else ''}")

    if args.max is not None and len(q.questions) > args.max:
        q.questions = random.choices(q.questions, k=args.max)
        logger.info(f"Picked {args.max} question{'s' if (args.max != 1) else ''}")

    logger.debug(f"Questions: {q.questions}")

    save_quiz(q, config["pickle-file"])


if __name__ == '__main__':
    main()
