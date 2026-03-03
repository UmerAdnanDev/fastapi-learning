from fastapi import FastAPI,Header
from typing import Optional
from pydantic import BaseModel
#uvicorn Basics.main:app --reload to run app on default port 8000 
#fastapi dev for single app to run on 8000 port
# add --port 8001 for a different port i.e 8001
#uvicorn Basics.basics:app --reload --port 8000   (if file is basics.py)
app = FastAPI()
# basic get request returning a text
# http://127.0.0.1:8000/
@app.get('/')
async def home():
  return {'Welcome to Home Page'}
# basic get request returning a dict / json data 
#http://127.0.0.1:8000/dict
@app.get('/dict')
def dic():
  return {'dict':'This is a python dictionary'}

# using name string type of path variable
# http://127.0.0.1:8000/greeting/Adnan 
@app.get('/greeting/{name}')
async def greet(name:str) -> dict:
  return {"greeting": f"Hi , {name}"}

# using age int type of path variable 
# http://127.0.0.1:8000/age/19 
@app.get("/age/{age}")
async def age(age:int) -> dict:
  return {"your age is ": age}

#using query parameter to send data/ value
#http://127.0.0.1:8000/usequery?name=umer&age=19
@app.get("/usequery")
async def querycheck(name:str,age:int)-> dict:
  return {"message":f"Your name is {name} and age is {age}"}

'''using Optional for default values of variables to avoid null error if no query entered'''
#http://127.0.0.1:8000/opquery
# or http://127.0.0.1:8000/opquery?name=umer&age=19 or either 
@app.get("/opquery")
async def optionalquery(name:Optional[str]="Default-Name",age:Optional[int]=0)-> dict:
  return {"message":f"Your name is {name} and age is {age}"}
#same thing even without optional but here is a difference 
'''in Optional use name variable can be either str or None (Empty)
 but without it it needs to be string (str)
(either in default value or web query ?age = None is possible in Optinal method)'''
@app.get("/noquery")
async def noquery(name:str ="Default-Name",age:int=0)-> dict:
  return {"message":f"Your name is {name} and age is {age}"}

class ProductModel(BaseModel): # A model to create products 
  product_name : str
  price : float
# A post request to create 
@app.post('/create_product')
async def cp(product_data:ProductModel):
  return{
    "name":product_data.product_name,
    "price":product_data.price
  }
@app.get('/get-headers',status_code=200) #can specify the status code 200,500..etc or random code
#Note: if it returns a random status code like 123 which is not a recognized status code then you will get , Parse Error:The server returned a malformed response 
async def get_headers(
  accept:str = Header(None),
  content_type:str = Header(None),
  user_agent:str = Header(None),
  host:str = Header(None)
):
   request_headers = {}
   request_headers["Accept"] = accept #tells server what content type the client can understand i.e application/json, text/html
   request_headers["Content-Type"] = content_type # format of request body i.e application/json 
   request_headers["User-Agent"] =user_agent # client browser/application in my case it is PostmanRuntime/7.51.1
   request_headers["Host"]=host # domain name of server
   return request_headers
'''Headers are metadata sent along with HTTP requests and responses.
  They contain important information about the request/response, 
 the client, and how the data should be handled.'''
# here header is extracted from http request and returned as json response

'''
__init__.py make the Basics folder into
a package from which modules can be imported
'''
#netstat -ano | findstr :8000 to check if app running on that port
#taskkill /PID 24392 /F add port id to kill it 