# For more information on getting data from the igsdb please see igsdb.lbl.gov/openapi
igsdb_api_token = "INSERT_YOUR_API_TOKEN_HERE"
url_single_product = "https://igsdb.lbl.gov/api/v1/products/{id}"  # Template URL for single product
url_single_product_datafile = "https://igsdb.lbl.gov/api/v1/products/{id}/datafile"  # Template URL for getting data file for a product
headers = {"Authorization": "Token {token}".format(token=igsdb_api_token)}  # Token authorization headers
