import sys
import os
import http.client
import dotenv
dotenv.load_dotenv(".env")

if not len(sys.argv) == 2:
    print(f"This script requires exactly 1 commandline argument, but got {len(sys.argv) - 1}")
    sys.exit()


def send( message ):
 
    # your webhook URL
    webhookurl = os.environ["WEBHOOK"]
 
    # compile the form data (BOUNDARY can be anything)
    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"
  
    # get the connection and make the request
    connection = http.client.HTTPSConnection("discordapp.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
        })
  
    # get the response
    response = connection.getresponse()
    result = response.read()
  
    # return back to the calling function with the result
    return result.decode("utf-8")
 
# send the messsage and print the response
print( send( sys.argv[1] ) )
