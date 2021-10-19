import os

dic = {
  'db_user' : os.environ["CLOUD_SQL_USERNAME"],
  'db_pass' : os.environ["CLOUD_SQL_PASSWORD"],
  'db_name' : os.environ["CLOUD_SQL_DATABASE_NAME"]
  }

for item in dic:
  print(item,dic[item])

