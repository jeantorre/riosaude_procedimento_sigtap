import os

import pandas as pd


def extract_tb_procedimento_layout(mes: str) -> pd.DataFrame:
    metadata_path = f"backend/data/TabelaUnificada_{mes}/"
    metadata_file = "tb_procedimento_layout.txt"
    metadata_tb_procedimento = metadata_path + metadata_file
    specs_df = pd.read_csv(metadata_tb_procedimento)
    return specs_df


def generate_colspecs(specs_df: pd.DataFrame) -> list:
    colspecs = [
        (start - 1, end) for start, end in zip(specs_df["Inicio"], specs_df["Fim"])
    ]
    return colspecs


def get_column_names(specs_df: pd.DataFrame) -> list:
    return specs_df["Coluna"].tolist()


def extract_tb_procedimento(
    mes: str, colspecs: list, column_names: list
) -> pd.DataFrame:
    data_path = f"backend/data/TabelaUnificada_{mes}/"
    data_file = "tb_procedimento.txt"
    data_tb_procedimento = data_path + data_file
    data_df = pd.read_fwf(
        data_tb_procedimento, colspecs=colspecs, names=column_names, encoding="latin1"
    )

    for col in ["VL_SH", "VL_SA", "VL_SP"]:
        data_df[col] = data_df[col].astype(float) / 100

    return data_df


def pipeline_tb_procedimento(mes: str) -> pd.DataFrame:
    specs_df = extract_tb_procedimento_layout(mes)
    colspecs = generate_colspecs(specs_df)
    column_names = get_column_names(specs_df)
    df = extract_tb_procedimento(mes, colspecs, column_names)

    return df


if __name__ == "__main__":
    mes = "202505"
    df = pipeline_tb_procedimento(mes)

    print(df.head())

    os.makedirs(
        "backend/data/processed/",
        exist_ok=True,
    )
    # df.to_csv(
    #     f"backend/data/processed/tb_procedimento_{mes}.csv",
    #     index=False,
    # )
