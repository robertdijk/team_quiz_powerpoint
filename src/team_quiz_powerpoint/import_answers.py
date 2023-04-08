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
    parser = argparse.ArgumentParser(description='Import answers from excel file')
    parser.add_argument('excelfile')
    parser.add_argument('-c', '--config', default=None, help="config file")
    args = parser.parse_args()

    config = load_config(args.config)

    q = load_quiz(config["pickle-file"])

    df = load_excel_file(Path(args.excelfile))
    df.columns = [title.rstrip() for title in df.columns]

    for index, row in df.iterrows():
        q.add_player_from_row(row, config["import"]["answers"]["fields"])

    logger.info(f"Imported {len(q.players)} player{'s' if (len(q.players) != 1) else ''}")

    save_quiz(q, config["pickle-file"])


if __name__ == '__main__':
    main()
