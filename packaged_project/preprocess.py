import pandas as pd

from coordinates_transform import tm128_to_wgs84

import re

class Preprocess(object):
    def __init__(self, category_query, category_query_dictlist):
        self.category_query = category_query
        self.category_query_dictlist = category_query_dictlist
    
    def remove_title_tags(self, df, match_list):
        for match in match_list:
            try:
                df['title'] = df['title'].apply(lambda x : re.sub(match, '', x))
            except:
                pass
        return df

    def add_category_query(self, df, category_query):        
        df['query_category'] = category_query    
        return df

    def category_divide(self, df):
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

        return df

    def df_naver_coordinates_transform_to_wgs84(self, df):
        """xy_coordinates_transform function transform based on epsg input,
           naver Katech coord is EPSG 5179
           WGS84 coord is EPSG 4326
           """
        df['longitude'] = tm128_to_wgs84(df['mapx'].values, df['mapy'].values)[0]
        df['latitude'] = tm128_to_wgs84(df['mapx'].values, df['mapy'].values)[1]
        return df
    
    def preprocess(self):
        cat_query_df = pd.DataFrame(self.category_query_dictlist).drop_duplicates()

        cat_query_df_p1 = self.remove_title_tags(cat_query_df, [r'<b>', r'</b>'])     
        cat_query_df_p2 = self.add_category_query(cat_query_df_p1, self.category_query)
        cat_query_df_p3 = self.category_divide(cat_query_df_p2)
        cat_query_df_p4 = self.df_naver_coordinates_transform_to_wgs84(cat_query_df_p3)

        drop_list = ['category', 'description', 'roadAddress', 'link', 'mapx', 'mapy', 'telephone', ]
        processed_df = cat_query_df_p4.drop(drop_list, axis=1).drop_duplicates(['longitude', 'latitude'])
        return processed_df