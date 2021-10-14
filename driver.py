import os
import app

print("Proxy booting...")
os.system("./cloud_sql_proxy -instances=dotted-vim-327120:us-central1:vote-caster-data=tcp:3306 &")
app.run()
