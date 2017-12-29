import pandas as pd


def get_category_query_list(brand_var_fp, infra_var_fp):
    if (brand_var_fp == None) or (infra_var_fp == None):
        raise ValueError("You must input target brand or infra query!")
    brand_query_list = list(pd.read_csv(brand_var_fp).values.flatten())
    infra_query_list = list(pd.read_csv(infra_var_fp).values.flatten())
    return brand_query_list, infra_query_list


def get_query_list(local_var_fp, category_query, dong_yn):
    local_category_query_lists = []
    
    if not local_var_fp:
        raise ValueError("You must input target local query!")
    
    if dong_yn:
        local_df = pd.read_csv(local_var_fp)
        for local_df_idx in local_df.index:
            sido = local_df.loc[local_df_idx, 'sido']
            gugun = local_df.loc[local_df_idx, 'gugun']
            dong = local_df.loc[local_df_idx, 'dong']
            temp_single_query = "{} {} {} {}".format(sido, gugun, dong, category_query)
            local_category_query_lists.append(temp_single_query)
    else:
        local_df = pd.read_csv(local_var_fp).loc[:, ['sido', 'gugun']].drop_duplicates()
        for local_df_idx in local_df.index:
            sido = local_df.loc[local_df_idx, 'sido']
            gugun = local_df.loc[local_df_idx, 'gugun']
            temp_single_query = "{} {} {}".format(sido, gugun, category_query)
            local_category_query_lists.append(temp_single_query)

    return local_category_query_lists