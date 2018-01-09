import pandas as pd
import numpy as np

from config.config_20171221 import DEFAULTS

from query import GetQuery
from api_requests import get_api_id_secret, NaverRequests
from preprocess import Preprocess
from mongodb import save_to_mongodb

from config.config_20171221 import DEFAULTS_MAP
from config.map_config_20171227 import BYBRAND_COLLECTION, POLY_CONDIDTION_BYBRAND_COLLECTION, INFRA_ADDED_BYBRAND_COLLECTION

from mongodb import mongo_find_to_df
from clustering import get_hdbscan_cluster_index, get_partial_silhouette_score
from mapping import (df_to_gdf_with_lon_lat_point, divide_gdf, GeoProcessing, get_clus_pivot_count_df, slicer,
                     slice_to_map)


TARGET_BRAND_CSV_FP = DEFAULTS['TARGET_BRAND_CSV_FP']
TARGET_INFRA_CSV_FP = DEFAULTS['TARGET_INFRA_CSV_FP']
TARGET_SIDO_GUGUN_DONG_CSV_FP = DEFAULTS['TARGET_SIDO_GUGUN_DONG_CSV_FP']
MONGODB_USERNAME = DEFAULTS['MONGODB_USERNAME']
MONGODB_PASSWORD = DEFAULTS['MONGODB_PASSWORD']
MONGODB_DBNAME = 'testdb'   #  DEFAULTS['MONGODB_DBNAME']


def api_connection_check():
    pass


def mongodb_connection_check():
    pass

    
# query check & logs 
def single_query_result_logs(query_result_dictlist, total_trial, count):
    pass 
    

def single_query_result_df_logs(query_result_dictlist_len, category_query, category_dict, processed_df_shape):
    pass


def controler_1(loc_fp, cat_fp, mongo_username, mongo_password, dbname, collectionname):
    query_dict = GetQuery(loc_fp, cat_fp).get_final_query_dict_bygugun()
    
    i = 0
    for category_query, local_category_query_list in query_dict.items():
        i += 1
        api_id, api_secret = get_api_id_secret(i)
        display = 10        
        category_query_dictlist =  NaverRequests(
                                        api_id, 
                                        api_secret, 
                                        local_category_query_list, 
                                        display).get_category_query()        
        
        if len(category_query_dictlist) < 1:
            print("{} / {} : {}, items : 0 #### Failed".format(
                i, len(query_dict.items()), category_query))
            pass
        else:
            processed_df = Preprocess(
                            category_query, 
                            category_query_dictlist).preprocess()
            
            save_to_mongodb(processed_df, 
                            username=mongo_username, 
                            userpassword=mongo_password, 
                            dbname=dbname, 
                            collectionname=collectionname)
            
            print("{} / {} : {}, items : {}".format(
                i, len(query_dict.items()), category_query, processed_df.shape[0]))
            
            
################################### After Mongo DB save ###################################


def cluster_result_logs(silhouette_score, category, count):
    pass


def controler_2(**DEFAULTS_MAP):
    df1 = mongo_find_to_df(DEFAULTS_MAP['username'],
                          DEFAULTS_MAP['userpassword'], 
                          DEFAULTS_MAP['dbname'], 
                          DEFAULTS_MAP['collectionname1'])
    df2 = mongo_find_to_df(DEFAULTS_MAP['username'],
                          DEFAULTS_MAP['userpassword'],
                          DEFAULTS_MAP['dbname'],
                          DEFAULTS_MAP['collectionname2'],
                          DEFAULTS_MAP['query'])
    gdf = df_to_gdf_with_lon_lat_point(pd.concat([df1, df2], axis=0))
    labels, X = get_hdbscan_cluster_index(gdf, 
                              min_cluster_size=DEFAULTS_MAP['min_cluster_size'], 
                              min_samples=DEFAULTS_MAP['min_samples'], 
                              metric=DEFAULTS_MAP['metric'])
    
    silhouette_score = get_partial_silhouette_score(labels, X)
    category, count = np.unique(labels, return_counts=True)    
    cluster_result_logs(silhouette_score, category, count)
    
    clustered_gdf, outliers_gdf = divide_gdf(gdf, labels)
    
    try:
        clus_polygon_gdf = GeoProcessing().get_clus_polygon_gdf(clustered_gdf)
        clus_label_query_count_df = get_clus_pivot_count_df(clustered_gdf, 'query_category')
        clus_label_category_count_df = get_clus_pivot_count_df(clustered_gdf, 'category_1')
    except:
        raise ValueError("Something wrong in clus category")
    
    try:
        for condition in BYBRAND_COLLECTION:
            slice_to_map(clus_polygon_gdf, 
                         clus_label_query_count_df, 
                         clus_label_category_count_df, 
                          **condition)
    except:
        raise ValueError("Bybrand Dataset is out of the criteria")
    
    try:
        # ** use bybrand collection condition for first slicing **
        for condition in POLY_CONDIDTION_BYBRAND_COLLECTION:
            clus_polygon_gdf_temp, clus_label_query_count_df_temp, clus_label_category_count_df_temp = slicer(
                                                                                                    clus_polygon_gdf, 
                                                                                                    clus_label_query_count_df, 
                                                                                                    clus_label_category_count_df,
                                                                                                    **condition[0])
            slice_to_map(clus_polygon_gdf_temp, 
                         clus_label_query_count_df_temp, 
                         clus_label_category_count_df_temp,
                         **condition[1])
    except:
        raise ValueError("Data for poly conditional maps aren't properly handled")
    
    try:
        if '지하철역' in clus_label_query_count_df.columns:
            for condition in INFRA_ADDED_BYBRAND_COLLECTION:
                 slice_to_map(clus_polygon_gdf_temp, 
                              clus_label_query_count_df_temp, 
                              clus_label_category_count_df_temp,
                              **condition)
    except:
        raise ValueError("Infra Dataset is not properly processed for mapping")
        
    return True
            
        
# print("{} : {}".format('sido', TARGET_SIDO_GUGUN_DONG_CSV_FP))
# print("{} : {}".format('brand', TARGET_BRAND_CSV_FP))
# print("{} : {}".format('infra', TARGET_INFRA_CSV_FP))
# print("{} : {}".format('muser', MONGODB_USERNAME))
# print("{} : {}".format('mpass', MONGODB_PASSWORD))
# print("{} : {}".format('mdbname', MONGODB_DBNAME))


if __name__ == "__main__":
    # controler_1(loc_fp=TARGET_SIDO_GUGUN_DONG_CSV_FP,
    #           cat_fp=TARGET_BRAND_CSV_FP,
    #           mongo_username=MONGODB_USERNAME,
    #           mongo_password=MONGODB_PASSWORD,
    #          dbname=MONGODB_DBNAME,
    #          collectionname='bybrand')
    #
    # controler_1(loc_fp=TARGET_SIDO_GUGUN_DONG_CSV_FP,
    #           cat_fp=TARGET_INFRA_CSV_FP,
    #           mongo_username=MONGODB_USERNAME,
    #           mongo_password=MONGODB_PASSWORD,
    #          dbname=MONGODB_DBNAME,
    #          collectionname='infra')
    
    if controler_2(**DEFAULTS_MAP):
        print("Mapping Done")
