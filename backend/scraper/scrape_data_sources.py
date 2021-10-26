import numpy as np
import pandas as pd
import yaml
import requests
import zipfile
import io
import os
import sys
import ssl
from os.path import join

ssl._create_default_https_context = ssl._create_unverified_context

next_index = 0

# data manipulation functions
all_names = []
output_dir = "excel_outputs"


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
                if xwalk[data_source][i] == "record_type":
                    df[xwalk[data_source][i]] = configs["sources"][data_source][
                        "type"
                    ]
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


def extract_all_subfolders(head_directory, data_source, xwalk, dat, configs):
    if os.path.isdir(head_directory):
        for filename in os.listdir(head_directory):
            if (
                configs["sources"][data_source]["subdirectory"] not in filename
                and configs["sources"][data_source]["subdirectory"] != "None"
            ):
                continue
            if dat is None or len(dat) == 0:
                dat = extract_all_subfolders(
                    join(head_directory, filename),
                    data_source,
                    xwalk,
                    dat,
                    configs,
                )
            else:
                dat = dat.append(
                    extract_all_subfolders(
                        join(head_directory, filename),
                        data_source,
                        xwalk,
                        dat,
                        configs,
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
    elif head_directory.endswith("csv"):
        data = pd.read_csv(head_directory, nrows=1048576)
        return data


def make_tables_data_source(data_source, xwalk, configs):
    print("Processing data source " + data_source)
    if configs["sources"][data_source]["url"].endswith(".xlsx"):
        dat_raw = pd.read_excel(configs["sources"][data_source]["url"])
        dat_raw.to_excel(join(output_dir, data_source + "_raw.xlsx"))
        dat = map_varnames(dat_raw, data_source, xwalk, configs)
        dat = gen_ids(dat, data_source)
    elif configs["sources"][data_source]["url"].endswith(".zip"):
        r = requests.get(configs["sources"][data_source]["url"])
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(
            join(output_dir, configs["sources"][data_source]["location"])
        )
        dat_raw = extract_all_subfolders(
            join(output_dir, configs["sources"][data_source]["headdirectory"]),
            data_source,
            xwalk,
            [],
            configs,
        )
        dat_raw = (
            dat_raw.groupby([configs["sources"][data_source]["id"]])
            .first()
            .reset_index()
        )
        dat = map_varnames(dat_raw, data_source, xwalk, configs)
        dat = gen_ids(dat, data_source)
    elif configs["sources"][data_source]["url"].endswith(".csv"):
        dat_raw = pd.read_csv(configs["sources"][data_source]["url"])
        dat_raw.to_excel(join(output_dir, data_source + "_raw.xlsx"))
        for i in range(xwalk.shape[0]):
            if xwalk[data_source][i] not in dat_raw.columns:
                dat_raw[xwalk[data_source][i]] = ""
            if xwalk[data_source][i] == "record_type":
                dat_raw[xwalk[data_source][i]] = configs["sources"][
                    data_source
                ]["type"]
        dat = map_varnames(dat_raw, data_source, xwalk, configs)
        dat = gen_ids(dat, data_source)

    dat = dat.loc[~dat.index.duplicated(keep="first")]
    dat.to_csv(join(output_dir, data_source + ".csv"), index=True, header=True)
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
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    xwalk = pd.read_csv(configs["resources"]["varname_crosswalk"])

    # make data tables
    data_sources = list(configs["sources"].keys())
    data_list = [
        make_tables_data_source(x, xwalk, configs) for x in data_sources
    ]

    table_names = list(configs["tables"].keys())
    table_list = [pd.concat([d[t] for d in data_list]) for t in table_names]
    table_dict = dict(zip(table_names, table_list))
    df_combine = pd.concat([table_dict["victim"], table_dict["incident"]])
    victim_indices = df_combine["victim_name_full"] != "Name withheld by police"
    victim_indices_2 = df_combine["victim_name_full"] != ""
    victim_indices_3 = df_combine["victim_name_full"].notnull()
    victim_indices_4 = df_combine["incident_date"].notnull()
    filtered_indices = (
        victim_indices & victim_indices_2 & victim_indices_3 & victim_indices_4
    )
    df_filtered = pd.concat(
        [
            df_combine[
                df_combine["victim_name_full"] == "Name withheld by police"
            ],
            df_combine[df_combine["victim_name_full"] == ""],
            df_combine[df_combine["victim_name_full"].isnull()],
            df_combine[df_combine["incident_date"].isnull()],
            df_combine[filtered_indices].drop_duplicates(
                ["victim_name_full", "incident_date"], keep="first"
            ),
        ]
    )
    df_filtered = df_filtered[~df_filtered.index.duplicated(keep="first")]
    final_indices = df_filtered.index

    # Write each dataframe to a different worksheet.
    excel_path = join(output_dir, "full_database.xlsx")
    writer = pd.ExcelWriter(excel_path, engine="xlsxwriter")
    print("Exporting results to " + excel_path)
    sheets = []
    for key in table_dict:
        sheet = table_dict[key].loc[final_indices]
        sheet.to_excel(writer, sheet_name=key)
        sheets.append(sheet)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    # Write all sheets to a single pickled dataframe, which loads faster than
    # xlsx.
    pickle_path = join(output_dir, "full_database.pkl.zip")
    print("Exporting to " + pickle_path)
    pd.concat(sheets, axis=1).to_pickle(pickle_path)

    return table_dict


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Too many arguments")
        sys.exit()
    if len(sys.argv) == 2:
        output_dir = sys.argv[1]
    else:
        print("defaulting output directory to " + output_dir)
    make_all_tables()
