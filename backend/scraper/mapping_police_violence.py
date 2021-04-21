import numpy as np
import pandas as pd
import yaml

# data manipulation functions


def map_varnames(df, data_source, xwalk):
    # clean column names
    df.columns = (
        df.columns.str.replace(" ", "_")
        .str.replace("[^\\d\\w]", "")
        .str.lower()
    )
    assert all(xwalk["mpv"].isin(df.columns))

    # select and map column names
    name_map = {
        xwalk[data_source][i]: xwalk["common"][i] for i in range(xwalk.shape[0])
    }
    df = df[xwalk[data_source].tolist()].rename(columns=name_map)
    return df


def gen_ids(df, data_source):
    # TODO: Decide how to make these ids, ex hashing columns
    df["data_source_id"] = data_source
    df["incident_id"] = np.nan
    df["victim_id"] = np.nan
    df["death_id"] = np.nan
    return df


# make tables functions


def make_single_table(table, dat, configs):
    assert all([x in dat.columns for x in configs["tables"][table]["required"]])
    cols = (
        configs["tables"][table]["required"]
        + configs["tables"][table]["optional"]
    )
    return dat[dat.columns[dat.columns.isin(cols)]]


def make_tables_data_source(data_source, xwalk, configs):
    dat_raw = pd.read_excel(configs["sources"][data_source]["url"])
    dat = map_varnames(dat_raw, data_source, xwalk)
    dat = gen_ids(dat, data_source)

    table_names = list(configs["tables"].keys())
    table_list = [make_single_table(x, dat, configs) for x in table_names]
    table_dict = {table_names[i]: table_list[i] for i in range(len(table_list))}

    return table_dict


def make_all_tables():
    """Pulls public data and combines into data table for relational databases
    output: dict of dataframes, one element per table described in configs
    """

    # read configs
    with open(r"backend/pull-public-data/configs.yaml") as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)
    xwalk = pd.read_csv(configs["resources"]["varname_crosswalk"])

    # make data tables
    data_sources = list(configs["sources"].keys())
    data_list = [
        make_tables_data_source(x, xwalk, configs) for x in data_sources
    ]
    table_names = list(configs["tables"].keys())
    table_list = [pd.concat([d[t] for d in data_list]) for t in table_names]
    table_dict = {table_names[i]: table_list[i] for i in range(len(table_list))}

    return table_dict


if __name__ == "__main__":
    make_all_tables()
