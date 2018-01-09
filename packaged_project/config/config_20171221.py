DEFAULTS = {
    'TARGET_BRAND_CSV_FP' : './csv_input/brand_20171221.csv',
    'TARGET_INFRA_CSV_FP' : './csv_input/infra_20171221.csv',
    'TARGET_SIDO_GUGUN_DONG_CSV_FP' : './csv_input/sido_gugun_dong_20171221.csv',
    'MONGODB_USERNAME' : '',
    'MONGODB_PASSWORD' : '',
    'MONGODB_DBNAME' : 'seoulmarketanalysis'
}

DEFAULTS_API = {
    'NUM': 5,
    'API_ID' : [
        '6MDkAOqz2_LTCSJxe7z9', 
        'TQLUfAMmGIq7o7ax4O5G', 
        'QnMrbbB_iCeVAKf8L0OT', 
        'aIupKzB__UU93OFuGD6b', 
        'iNuroJPuZQwULrg2GMEx'],
    'API_SECRET' : [
        '', 
        '', 
        '', 
        '', 
        ''] 
}

DEFAULTS_MAP = {
          'username': 'kadencho', 
          'userpassword': '', 
          'dbname': '', 
          'collectionname1': '',
          'collectionname2': '',
          'query': { 'query_category' : '지하철역' },
            'min_cluster_size': 20,
            'min_samples': 2,
            'metric': 'haversine'
                }
