import boto3,json 
from pg import DB 

secret_name = 'secret_name'
region_name ='ap-southeast-2'

session = boto3.session.Session()

client = session.client(service_name='secretsmanager',region_name=region_name)

get_secret_value_response = client.get_secret_value(SecretId=secret_name)

creds = json.loads(get_secret_value_response['SecretString'])

username = creds['username']
password = creds['password']
host = creds['host']

db = DB(dbname='dev',host=host,port=5439,user=username,passwd=password)

merge_qry = """
			begin ; 
			copy mysql_dwh.geolocation from 's3://bucket-name/geolocation/historical/geolocation.csv'
			iam_role 'YOUR_ARN'
			CSV QUOTE '\"' DELIMITER ','
			acceptinvchars;
			end ; 
			"""

result = db.query(merge_qry)
print(result)
