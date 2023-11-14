from pathlib import Path
import pandas as pd
from numpy.typing import NDArray
import numpy as np
from io import StringIO
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)


def _find_number_of_level(df: pd.DataFrame) -> int:
    logger.debug("Modification inplace of the dataframe")
    level_counts = df.iloc[:, 0].str.len().value_counts()
    df["level"] = np.zeros(len(df), dtype=np.int32)
    for k in range(len(level_counts)):
        df.loc[df.iloc[:, 0].str.len() == (k + 1), "level"] = k
    return len(level_counts)


def _extract_df(df: pd.DataFrame, key: str, current_level: int) -> pd.DataFrame:
    row_for_df = []
    begin_extraction = False
    first_column = df.columns[0]
    for row_id, row in df.iterrows():
        if begin_extraction:
            if row["level"] > current_level:
                row_for_df.append(row)
            else:
                return pd.DataFrame(row_for_df)
        if row[first_column] == key:
            begin_extraction = True
    return pd.DataFrame(row_for_df)


def _build_mapping(df: pd.DataFrame, current_level: int, max_level: int):
    if current_level == max_level:
        if len(df) == 0:
            return []
        return list(df.loc[df["level"] == current_level, df.columns[0]])
    keys = list(df.loc[df["level"] == current_level, df.columns[0]])
    return OrderedDict(
        (
            (
                key,
                _build_mapping(
                    _extract_df(df, key, current_level),
                    current_level + 1,
                    max_level,
                ),
            )
            for key in keys
        )
    )


def build_data_from_hierarchical_csv(
    file_path: str | Path, header: int | None = None
) -> tuple[int, dict[int, OrderedDict[str, str]], OrderedDict[str, OrderedDict]]:
    """
    Build data from a csv having the following format
    level_0_item_1
    level_1_item_1
    level_2_item_1
    level_2_item_2
    level_1_item_2
    level_2_item_3
    level_2_item_4
    level_0_item_2

    Returns dictionnary for each level and a mapping dictionnary containing the tree structure.
    """
    df = pd.read_csv(file_path, header=header)
    df.iloc[:, 0] = df.iloc[:, 0].astype(str)
    n_level = _find_number_of_level(df)
    levels_dict = {}
    for k in range(n_level):
        levels_dict[k] = OrderedDict(
            df.loc[df["level"] == k, [df.columns[0], df.columns[1]]].to_records(
                index=False
            )
        )
    mapping_dict = _build_mapping(df, 0, n_level - 1)
    return n_level, levels_dict, mapping_dict


if __name__ == "__main__":
    csv = StringIO(
        """
"A","Agriculture, forestry and fishing"
"01","Crop and animal production, hunting and related service activities"
"011","Growing of non-perennial crops"
"0111","Growing of cereals (except rice), leguminous crops and oil seeds"
"0112","Growing of rice"
"0113","Growing of vegetables and melons, roots and tubers"
"0114","Growing of sugar cane"
"0115","Growing of tobacco"
"0116","Growing of fibre crops"
"0119","Growing of other non-perennial crops"
"012","Growing of perennial crops"
"0121","Growing of grapes"
"0122","Growing of tropical and subtropical fruits"
"0123","Growing of citrus fruits"
"0124","Growing of pome fruits and stone fruits"
"0125","Growing of other tree and bush fruits and nuts"
"0126","Growing of oleaginous fruits"
"0127","Growing of beverage crops"
"0128","Growing of spices, aromatic, drug and pharmaceutical crops"
"0129","Growing of other perennial crops"
"013","Plant propagation"
                   """
    )
    n_level, levels_dict, mapping_dict = build_data_from_hierarchical_csv(
        csv, header=None
    )
