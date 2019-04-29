#curl -X POST -d "pass[]=123" http://chinalover.sinaapp.com/web21/
# or
import requests
res = requests.post("http://chinalover.sinaapp.com/web21/",data="pass[]=123")
print(res.content)
