import pandas as pd
import numpy as np


class GetQuery(object):
    def __init__(self, loc_fp, cat_fp):
        self.loc_fp = loc_fp
        self.cat_fp = cat_fp
        
    def get_local_query_array(self, fp):
        try:
            temp_loc_df = pd.read_csv(fp).loc[:, ['sido', 'gugun']].drop_duplicates()
            local_query_array = np.apply_along_axis(lambda x : ' '.join(x), 1, temp_loc_df.values).astype('object')    
        except:
            raise FileNotFoundError("{} does not exists".format(fp))
        return local_query_array        
    
    def get_category_query_array(self, fp):
        try:
            categories_query_array = pd.read_csv(fp).astype('object').values.flatten()
        except:
            raise FileNotFoundError("{} does not exists".format(fp))
        return categories_query_array
     
    def get_final_query_dict_bygugun(self):
        local_query_array = self.get_local_query_array(self.loc_fp)
        categories_query_array = self.get_category_query_array(self.cat_fp)
        final_query_dict_bygugun = {}
        for category in categories_query_array:
            local_category_query_array = local_query_array + ' ' + category
            final_query_dict_bygugun[category] = list(local_category_query_array)
        return final_query_dict_bygugun