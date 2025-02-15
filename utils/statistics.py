def get_statistics(df_ag, year):
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
    dest.loc[-1] = get_statistics(source, year)
    dest.index = dest.index + 1
    return dest