import pandas as pd

from coordinates_transform import tm128_to_wgs84

import re


def remove_title_tags(df, match_list):
    for match in match_list:
        try:
            df['title'] = df['title'].apply(lambda x : re.sub(match, '', x))
        except:
            pass
    return df


def add_category_query(df, category_query):        
    df['query_category'] = category_query    
    return df


def category_divide(df):
    category_dict = {}
    try:
        df['category_1'] = df['category'].apply(lambda x : str(x).strip('>').split('>')[0])
    except:
        pass  
    
    try:        
        df['category_2'] = df[['category']].loc[df['category'].apply(
            lambda x : len(str(x).strip('>').split('>'))) == 2, 'category'].apply(
            lambda x : str(x).strip('>').split('>')[1])
        df['category_2'] = df['category_2'].fillna('없음')
    except:
        pass
    
    category_unique = df[['category_1', 'category_2']].drop_duplicates().dropna()
    
    for category_1 in category_unique['category_1']:
        category_2 = category_unique.loc[category_unique['category_1'] == category_1, 'category_2'].values[0]
        if not category_1:
            break
        elif category_1 not in category_dict.keys():
            if not category_2:
                category_dict[category_1] = ['no value']
            else:
                category_dict[category_1] = [category_2]
        else:
            if not category_2:
                break
            elif category_2 not in category_dict[category_1]:
                category_dict[category_1].append(category_2)
            else:
                pass
    return df, category_dict


def df_naver_coordinates_transform_to_wgs84(df):
    """xy_coordinates_transform function transform based on epsg input,
       naver Katech coord is EPSG 5179
       WGS84 coord is EPSG 4326
       """
    df['longitude'] = tm128_to_wgs84(df['mapx'].values, df['mapy'].values)[0]
    df['latitude'] = tm128_to_wgs84(df['mapx'].values, df['mapy'].values)[1]
    return df

    
def preprocess(query_result_dictlist, category_query):
    query_result_dictlist_len = len(query_result_dictlist)
    query_result_df = pd.DataFrame(query_result_dictlist).drop_duplicates()
    if query_result_df is not None:
        del query_result_dictlist
    
    query_result_df_p1 = remove_title_tags(query_result_df, [r'<b>', r'</b>'])        
    query_result_df_p2 = add_category_query(query_result_df_p1, category_query)
    query_result_df_p3, category_dict = category_divide(query_result_df_p2)
    query_result_df_p4 = df_naver_coordinates_transform_to_wgs84(query_result_df_p3)
    
    drop_list = ['category', 'description', 'roadAddress', 'link', 'mapx', 'mapy', 'telephone', ]
    processed_df = query_result_df_p4.drop(drop_list, axis=1).drop_duplicates(['longitude', 'latitude'])
    
    return processed_df, query_result_dictlist_len, category_query, category_dict