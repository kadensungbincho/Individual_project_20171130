# mapping details
OUTPUT_FP = './templates/maps/'

large_area = {'_slice' : True,
              'criteria' : 'geometry',
              'column_name' : 'area',
              'method' : 'numeric',
              '_range' : 'up',
              'up_limit' : 0.5,
              'down_limit' : None,
              'layer_name' : 'large_area',
              'visualization' : 'category',
              'out_fp' : OUTPUT_FP}

medium_area = {'_slice' : True,
              'criteria' : 'geometry',
              'column_name' : 'area',
              'method' : 'numeric',
              '_range' : 'mid',
              'up_limit' : 0.5,
              'down_limit' : 0.25,
              'layer_name' : 'medium_area',
              'visualization' : 'category',
              'out_fp' : OUTPUT_FP}

small_area = {'_slice' : True,
              'criteria' : 'geometry',
              'column_name' : 'area',
              'method' : 'numeric',
              '_range' : 'down',
              'up_limit' : None,
              'down_limit' : 0.25,
              'layer_name' : 'small_area',
              'visualization' : 'category',
              'out_fp' : OUTPUT_FP}

dense_large_area = [{'column_name' : 'area',
              'method' : 'numeric',
              '_range' : 'mid',
              'up_limit' : 0.5,
              'down_limit' : 0.25},
                    {'_slice' : True,
              'criteria' : 'geometry',
              'column_name' : 'density',
              'method' : 'sort',
              '_range' : None,
              'up_limit' : 20,
              'down_limit' : None,
              'layer_name' : 'dense_large_area',
              'visualization' : 'category',
              'out_fp' : OUTPUT_FP}]

dense_medium_area = [{'column_name' : 'area',
              'method' : 'numeric',
              '_range' : 'up',
              'up_limit' : 0.5,
              'down_limit' : None},
                     {'_slice' : True,
              'criteria' : 'geometry',
              'column_name' : 'density',
              'method' : 'sort',
              '_range' : None,
              'up_limit' : 20,
              'down_limit' : None,
              'layer_name' : 'dense_medium_area',
              'visualization' : 'category',
              'out_fp' : OUTPUT_FP}]

subway_available = {'_slice' : True,
              'criteria' : 'query',
              'column_name' : '지하철역',
              'method' : 'numeric',
              '_range' : 'up',
              'up_limit' : 1.0,
              'down_limit' : None,
              'layer_name' : 'subway_available',
              'visualization' : 'category',
              'out_fp' : OUTPUT_FP}

subway_non_available = {'_slice' : True,
              'criteria' : 'query',
              'column_name' : '지하철역',
              'method' : 'numeric',
              '_range' : 'down',
              'up_limit' : None,
              'down_limit' : 0.5,
              'layer_name' : 'subway_non_available',
              'visualization' : 'category',
              'out_fp' : OUTPUT_FP}

BYBRAND_COLLECTION = [large_area, medium_area, small_area]
POLY_CONDIDTION_BYBRAND_COLLECTION = [dense_large_area, dense_medium_area]
INFRA_ADDED_BYBRAND_COLLECTION = [subway_available, subway_non_available]