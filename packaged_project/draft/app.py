import pandas as pd

from config.config_20171221 import DEFAULTS

from csv_to_query_list import get_category_query_list, get_query_list
from naver_api_requests import get_api_id_secret, get_api_dictlist
from preprocess import preprocess
from mongodb import save_to_mongodb


# TARGET_BRAND_CSV_FP = str(input("TARGET_BRAND_CSV_FP : "))
# TARGET_INFRA_CSV_FP = str(input("TARGET_INFRA_CSV_FP : "))
# TARGET_SIDO_GUGUN_DONG_CSV_FP = str(input("TARGET_SIDO_GUGUN_DONG_CSV_FP : "))
# API_ID = str(input("API_ID : "))
# API_SECRET = str(input("API_SECRET : "))
# MONGODB_USERNAME = str(input("MONGODB USERNAME : "))
# MONGODB_PASSWORD = str(input("MONGODB PASSWORD : "))

TARGET_BRAND_CSV_FP = DEFAULTS['TARGET_BRAND_CSV_FP']
TARGET_INFRA_CSV_FP = DEFAULTS['TARGET_INFRA_CSV_FP']
TARGET_SIDO_GUGUN_DONG_CSV_FP = DEFAULTS['TARGET_SIDO_GUGUN_DONG_CSV_FP']
MONGODB_USERNAME = DEFAULTS['MONGODB_USERNAME']
MONGODB_PASSWORD = DEFAULTS['MONGODB_PASSWORD']
MONGODB_DBNAME = DEFAULTS['MONGODB_DBNAME']


def api_connection_check():
    pass


def mongodb_connection_check():
    pass

    
# query check & logs 
def single_query_result_logs(query_result_dictlist, total_trial, count):
    pass 
    

def single_query_result_df_logs(query_result_dictlist_len, category_query, category_dict, processed_df_shape):
    pass
    


def controler(local_var_fp, brand_var_fp, infra_var_fp, mongo_username, mongo_password, dbname):
    brand_query_list, infra_query_list = get_category_query_list(brand_var_fp, infra_var_fp)
    category_query_list = brand_query_list + infra_query_list
    division_point_for_mongodb = len(category_query_list)
    
    api_connection_check()
    mongodb_connection_check()
    for i, category_query in enumerate(category_query_list[6:]): ########################################## check
        # get all query as a list
        if i < division_point_for_mongodb:
            dong_yn = False
        else:
            dong_yn = True
        local_category_query_lists = get_query_list(
            local_var_fp=local_var_fp, 
            category_query=category_query,
            dong_yn=dong_yn
        )    
        
        query_result_dictlist = []
        for local_category_query in local_category_query_lists:
            api_id, api_secret = get_api_id_secret(i)            
            display = 10 # default set 
            single_query_result_dictlist, total_trial, count = get_api_dictlist(
                                                    api_id=api_id, 
                                                    api_secret=api_secret, 
                                                    local_category_query=local_category_query, 
                                                    display=display)
            query_result_dictlist.extend(single_query_result_dictlist)
        if len(query_result_dictlist) < 1:
            print("{} / {} : {}, items : 0 #### Failed".format(i, len(category_query_list), category_query))
            pass
        else:
            processed_df = pd.DataFrame()
            # query request result logs
            single_query_result_logs(query_result_dictlist, total_trial, count)

            # preprocess each query
            processed_df, query_result_dictlist_len, category_query, category_dict = preprocess(query_result_dictlist, category_query)

            # preprocess logs 
            single_query_result_df_logs(query_result_dictlist_len, category_query, category_dict, processed_df.shape)

            dbname = dbname
            if i < division_point_for_mongodb:
                collectionname = 'bybrand'
            else:
                collectionname = 'byinfra'
            # save each preprocessed query to mongoDB
            save_to_mongodb(processed_df, 
                            username=mongo_username, 
                            userpassword=mongo_password, 
                            dbname=dbname, 
                            collectionname=collectionname)
            print("{} / {} : {}, items : {}".format(i, len(category_query_list), category_query, processed_df.shape[0]))
            
print("{} : {}".format('sido', TARGET_SIDO_GUGUN_DONG_CSV_FP))
print("{} : {}".format('brand', TARGET_BRAND_CSV_FP))
print("{} : {}".format('infra', TARGET_INFRA_CSV_FP))
print("{} : {}".format('muser', MONGODB_USERNAME))
print("{} : {}".format('mpass', MONGODB_PASSWORD))
print("{} : {}".format('mdbname', MONGODB_DBNAME))


if __name__ == "__main__":
    controler(local_var_fp=TARGET_SIDO_GUGUN_DONG_CSV_FP, 
              brand_var_fp=TARGET_BRAND_CSV_FP, 
              infra_var_fp=TARGET_INFRA_CSV_FP, 
              mongo_username=MONGODB_USERNAME, 
              mongo_password=MONGODB_PASSWORD,
             dbname=MONGODB_DBNAME)
    print("DONE")