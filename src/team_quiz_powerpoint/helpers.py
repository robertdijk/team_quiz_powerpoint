import itertools
from pathlib import Path

import pandas as pd


def iter_nth(iterable, nth):
    return next(itertools.islice(iterable, nth, nth + 1))


def load_excel_file(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, index_col=0)
    df = df.reset_index()
    return df
