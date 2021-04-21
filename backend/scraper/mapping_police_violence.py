import numpy as np
import pandas as pd
import yaml
import requests
import zipfile
import io
import os


# data manipulation functions


def map_varnames(df, data_source, xwalk):
    # clean column names
    df.columns = (
        df.columns.str.replace(" ", "_").str.replace
        ("[^\\d\\w]", "").str.lower()
    )
    # assert all(xwalk["mpv"].isin(df.columns))
    # assert all(xwalk["nyclu"].isin(df.columns))

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


def extract_all_subfolders(head_directory, data_source, xwalk, dat):
    if os.path.isdir(head_directory):
        for filename in os.listdir(head_directory):
            if "complaints" not in filename:
                continue
            if dat is None or len(dat) == 0:
                dat = extract_all_subfolders(
                    head_directory + "/" + filename, data_source, xwalk, dat)
            else:
                dat = dat.append(extract_all_subfolders(
                    head_directory + "/" + filename, data_source, xwalk, dat))
        return dat
    elif head_directory.endswith("csv.gz"):
        data = pd.read_csv(head_directory, nrows=1048576, compression='gzip',
                           error_bad_lines=False)
        print(data)
        return data


def make_tables_data_source(data_source, xwalk, configs):
    if configs["sources"][data_source]["url"].endswith(".xlsx"):
        dat_raw = pd.read_excel(configs["sources"][data_source]["url"])
        dat = map_varnames(dat_raw, data_source, xwalk)
        dat = gen_ids(dat, data_source)
    elif configs["sources"][data_source]["url"].endswith(".zip"):
        r = requests.get(configs["sources"][data_source]["url"])
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(".")
        dat_raw = extract_all_subfolders("fully-unified-data",
                                         data_source, xwalk, [])
        dat_raw['victims_name'] = ""
        dat_raw['cause_of_death'] = ""
        dat_raw['county'] = ""
        dat_raw = dat_raw.groupby(['cr_id']).first().reset_index()
        dat = map_varnames(dat_raw, data_source, xwalk)
        dat = gen_ids(dat, data_source)
        # dat.to_csv(r'cpdp_data.csv', index=False, header=True)
    table_names = list(configs["tables"].keys())
    table_list = [make_single_table(x, dat, configs) for x in table_names]
    table_dict = {table_names[i]: table_list[i] for i in range(len(table_list))}

    return table_dict


def make_all_tables():
    """Pulls public data and combines into data table for relational databases
    output: dict of dataframes, one element per table described in configs
    """

    # read configs
    with open(r"backend/scraper/configs.yaml") as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)
    xwalk = pd.read_csv(configs["resources"]["varname_crosswalk"])

    # make data tables
    data_sources = list(configs["sources"].keys())
    print("Sources: ")
    print(configs["sources"])
    data_list = [
        make_tables_data_source(x, xwalk, configs) for x in data_sources
    ]
    table_names = list(configs["tables"].keys())
    table_list = [pd.concat([d[t] for d in data_list]) for t in table_names]
    table_dict = {table_names[i]: table_list[i] for i in range(len(table_list))}
    # print(table_dict)
    return table_dict


if __name__ == "__main__":
    # print("in main")
    make_all_tables()
