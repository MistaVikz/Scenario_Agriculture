def get_statistics(df_ag, year):
    """
    Calculate statistics for a given DataFrame column and year.

    Args:
        df_ag (pd.Series): The DataFrame column to calculate statistics for.
        year (int): The year associated with the statistics.

    Returns:
        list: A list containing the year, max value, min value, median value,
              index of max value, index of min value, and index of median value.
    """
    max_value = df_ag.max()
    min_value = df_ag.min()
    median_value = df_ag.median()
    max_row = df_ag.idxmax()
    min_row = df_ag.idxmin()
    median_row = df_ag.sub(median_value).abs().idxmin()

    stats = []
    stats.append(year)
    stats.append(max_value)
    stats.append(min_value)
    stats.append(median_value)
    stats.append(max_row)
    stats.append(min_row)
    stats.append(median_row)

    return stats

def add_stats_to_df(dest, source, year):
    """
    Add statistics to a destination DataFrame from a source DataFrame column for a given year.

    Args:
        dest (pd.DataFrame): The destination DataFrame to add statistics to.
        source (pd.Series): The source DataFrame column to calculate statistics from.
        year (int): The year associated with the statistics.

    Returns:
        pd.DataFrame: The destination DataFrame with added statistics.
    """
    dest.loc[-1] = get_statistics(source, year)
    dest.index = dest.index + 1

    index_cols = dest.filter(regex="INDEX")
    for index_col in index_cols:
        dest[index_col] = dest[index_col].astype(int)

    return dest