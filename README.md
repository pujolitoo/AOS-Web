# aossample

## Sample FastAPI project


#Create virtual machine

python3 -m venv venv
source venv/bin/activate



Test using curl

curl -X GET "http://127.0.0.1:8000/concat?param1=Hello&param2=World"

Return 
{"result":"HelloWorld"}



You can test using the 