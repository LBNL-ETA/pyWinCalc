# For more information on getting data from the igsdb please see igsdb.lbl.gov/openapi
igsdb_api_token = "f91040beed231bc3f5a0e83cdb59af59ff1fab37"
url_single_product = "https://igsdb.lbl.gov/api/v1/products/{id}"  # Template URL for single product
url_single_product_datafile = "https://igsdb.lbl.gov/api/v1/products/{id}/datafile"  # Template URL for getting data file for a product
headers = {"Authorization": "Token {token}".format(token=igsdb_api_token)}  # Token authorization headers
