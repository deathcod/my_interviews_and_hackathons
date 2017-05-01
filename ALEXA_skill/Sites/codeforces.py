import requests
import json
import boto3
import decimal
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DynamoDB(object):
	"""docstring for DynamoDB"""

	def __init__(self, table_name, DEPLOY = False):
		super(DynamoDB, self).__init__() 
		self.table_name = table_name

		# this is to make the difference when working in local or server
		if DEPLOY:
			self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		else:
			self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")

		#this is any easy way to handle the exception, checking if the table is created or not
		try:
			self.create_table();
			pass
		except:
			pass
		pass

	def create_table(self):
		table = self.dynamodb.create_table(
			TableName = self.table_name,
			KeySchema = [
				{
					'AttributeName' : 'competiton_name',
					'KeyType' : 'HASH'  #Partition key
				},
				{
					'AttributeName' : 'datetime',
					'KeyType' : 'RANGE'	 #Sort Key
				}
			],
			AttributeDefinitions = [
				{
					'AttributeName' : 'competiton_name',
					'AttributeType' : 'S'
				},
				{
					'AttributeName' : 'datetime',
					'AttributeType' : 'N'
				}
			],
			ProvisionedThroughput = {
				'ReadCapacityUnits' : 10,
				'WriteCapacityUnits': 10
			}
		)
		print ("Table status:", table.table_status)

		pass

	def put_data(self, items ):

		table = self.dynamodb.Table(self.table_name)
		for i in items:
			response = table.put_item(Item = i)
			print ("Put item succeeded")
			print (json.dumps(response, indent = 4, cls = DecimalEncoder))
		pass

	def get_data(self , key):
		table = self.dynamodb.Table(self.table_name)
		try:
			response = table.get_item( Key = key)
			pass
		except ClientError as e:
			print(e.response['Error']['Message'])
		else:
			item = response['Item']
			print("GetItem succeeded:")
			print(json.dumps(item, indent=4, cls=DecimalEncoder))
			pass
		pass


def codeforces(DEPLOY = False):
	x = ""
	output = []

	if DEPLOY:
		x = requests.get("http://codeforces.com/api/contest.list?gym=false").text
	else:
		with open('input_codeforces.json','r') as f:
			x = f.read()
			pass
		pass

	j = json.loads(x)
	for i in j["result"]:
		if i["phase"] == "BEFORE" or i["phase"] == "CODING" :
			temp = {}
			temp["competiton_name"] = i["name"]
			temp["site_name"] = "codeforces"
			temp["datetime"] = i["startTimeSeconds"]
			temp["classification"] = "cp"
			temp["URL"] = " "
			output.append(temp)

	return (output)
	pass


def testing():

	#This is the main variable which changed to true all the changes will take place 
	#everywhere in the code and the code is ready to be uploaded.
	DEPLOY = True

	x = DynamoDB('competitons', DEPLOY = DEPLOY)
	x.put_data(codeforces(DEPLOY = False))
	x.get_data( {
					'competiton_name' : 'VK Cup 2017 - Wild Card Round 2',
					'datetime' : 1493220900
				})
	pass