import numpy as np
import pandas as pd
import yaml
import requests
import zipfile
import io
import os

next_index = 0

# data manipulation functions


def map_varnames(df, data_source, xwalk, configs):
    # clean column names
    df.columns = (
        df.columns.str.replace(" ", "_")
        .str.replace("[^\\d\\w]", "")
        .str.lower()
    )
    for i in range(xwalk.shape[0]):
        if xwalk[data_source][i] not in df.columns:
            df[xwalk[data_source][i]] = ""
            if xwalk[data_source][i] == "record_type":
                df[xwalk[data_source][i]] = xwalk[data_source]
                if xwalk[data_source][i] == 'record_type':
                    df[xwalk[data_source][i]]\
                        = configs["sources"][data_source]["type"]
    # assert all(xwalk["mpv"].isin(df.columns))
    # assert all(xwalk["nyclu"].isin(df.columns))

    # select and map column names
    name_map = {
        xwalk[data_source][i]: xwalk["common"][i] for i in range(xwalk.shape[0])
    }

    df = df[xwalk[data_source].tolist()].rename(columns=name_map)
    return df


def gen_ids(df, data_source):
    global next_index
    # TODO: Decide how to make these ids, ex hashing columns
    df["data_source_id"] = data_source
    df["incident_id"] = ""
    df["victim_id"] = np.nan
    df["death_id"] = np.nan
    df.set_index("incident_id", inplace=True)
    as_list = df.index.tolist()
    for v in range(0, len(as_list)):
        as_list[v] = next_index
        next_index = next_index + 1
    df.index = as_list

    return df


# make tables functions


def make_single_table(table, dat, configs):
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
                    head_directory + "/" + filename, data_source, xwalk, dat
                )
            else:
                dat = dat.append(
                    extract_all_subfolders(
                        head_directory + "/" + filename, data_source, xwalk, dat
                    )
                )
        return dat
    elif head_directory.endswith("csv.gz"):
        data = pd.read_csv(
            head_directory,
            nrows=1048576,
            compression="gzip",
            error_bad_lines=False,
        )
        return data


def make_tables_data_source(data_source, xwalk, configs):
    if configs["sources"][data_source]["url"].endswith(".xlsx"):
        dat_raw = pd.read_excel(configs["sources"][data_source]["url"])
        dat = map_varnames(dat_raw, data_source, xwalk, configs)
        dat = gen_ids(dat, data_source)
    elif configs["sources"][data_source]["url"].endswith(".zip"):
        r = requests.get(configs["sources"][data_source]["url"])
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(".")
        dat_raw = extract_all_subfolders(
            "fully-unified-data", data_source, xwalk, [])
        dat_raw = dat_raw.groupby(['cr_id']).first().reset_index()
        dat = map_varnames(dat_raw, data_source, xwalk, configs)
        dat = gen_ids(dat, data_source)
    elif configs["sources"][data_source]["url"].endswith(".csv"):
        dat_raw = pd.read_csv(configs["sources"][data_source]["url"])
        for i in range(xwalk.shape[0]):
            if xwalk[data_source][i] not in dat_raw.columns:
                dat_raw[xwalk[data_source][i]] = ""
            if xwalk[data_source][i] == 'record_type':
                dat_raw[xwalk[data_source][i]]\
                    = configs["sources"][data_source]["type"]
        dat = map_varnames(dat_raw, data_source, xwalk, configs)
        dat = gen_ids(dat, data_source)

    dat = dat.loc[~dat.index.duplicated(keep='first')]
    dat.to_csv(data_source + '.csv', index=True, header=True)
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
    data_list = [
        make_tables_data_source(x, xwalk, configs) for x in data_sources
    ]
    table_names = list(configs["tables"].keys())
    table_list = []
    for t in table_names:
        first_iteration = True
        sub_table_list = []
        for d in data_list:
            if first_iteration:
                full_df = d[t]
                first_iteration = False
            else:
                full_df = pd.concat([full_df, d[t]])
            sub_table_list.append(d[t])
        sub_table = full_df
        table_list.append(sub_table)
    table_dict = {table_names[i]: table_list[i] for i in range(len(table_list))}
    writer = pd.ExcelWriter('full_database.xlsx', engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    for key in table_dict:
        sub_data = table_dict[key]
        sub_data.to_excel(writer, sheet_name=key)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    return table_dict


if __name__ == "__main__":
    make_all_tables()
