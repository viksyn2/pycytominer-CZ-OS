import os
import random
import tempfile
import numpy as np
import pandas as pd
from pycytominer import consensus

random.seed(123)

# Get temporary directory
tmpdir = tempfile.gettempdir()

# Set example data
data_df = pd.DataFrame(
    {
        "Metadata_plate": ["a", "a", "a", "a", "b", "b", "b", "b"],
        "Metadata_treatment": [
            "drug",
            "drug",
            "control",
            "control",
            "drug",
            "drug",
            "control",
            "control",
        ],
        "Cells_x": [1, 2, 8, 2, 5, 5, 5, 1],
        "Cells_y": [3, 1, 7, 4, 5, 9, 6, 1],
        "Cytoplasm_z": [1, 8, 2, 5, 6, 22, 2, 2],
        "Nuclei_zz": [14, 46, 1, 6, 30, 100, 2, 2],
    }
).reset_index(drop=True)

consensus(
    data_df,
    replicate_columns="Metadata_treatment",
    operation="mean",
    output_file=output_test_file,
)


def test_consensus_aggregate():
    mean_df = consensus(
        data_df, replicate_columns="Metadata_treatment", operation="mean"
    )
    assert mean_df.shape == (2, 5)
    assert mean_df.loc[0, "Cells_x"] == 4.00
    pd.testing.assert_frame_equal(mean_df, pd.read_csv(output_test_file))

    median_df = consensus(
        data_df, replicate_columns="Metadata_treatment", operation="median"
    )
    assert median_df.shape == (2, 5)
    assert median_df.loc[0, "Cells_x"] == 3.5


def test_consensu_modz():
    modz_df = consensus(
        data_df, replicate_columns="Metadata_treatment", operation="modz"
    )
    assert modz_df.shape == (2, 5)
    assert modz_df.loc[0, "Cells_x"] == 3.7600

    modz_df = consensus(
        data_df,
        replicate_columns="Metadata_treatment",
        operation="modz",
        modz_precision=5,
    )
    assert modz_df.shape == (2, 5)
    assert np.round(modz_df.loc[0, "Cells_x"], 5) == 3.7602

    mean_df = consensus(
        data_df, replicate_columns="Metadata_treatment", operation="mean"
    )
    modz_df = consensus(
        data_df,
        replicate_columns="Metadata_treatment",
        operation="modz",
        modz_min_weight=1,
    )
    pd.testing.assert_frame_equal(modz_df, pd.read_csv(output_test_file))
