from chalice import Chalice, ChaliceViewError
from requests.structures import CaseInsensitiveDict
import requests
import threading
import json
import time

app = Chalice(app_name='odastudio')

# api-endpoint
bucket_id = "fY8JNWraEKcj"
URL = "https://pxlnwwd545.execute-api.us-east-2.amazonaws.com/api/buckets/" + bucket_id +"/files"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"

def patch(file, list):
    i = 0
    # If there is more than 10 attempted failures it should be a bigger problem                                                                                                                                                                     
    while i < 10:
        try:
            r = requests.patch(URL + '/' + file['id'], headers=headers, data=json.dumps(file))
        except:
            i+=1
            continue
        i += 1
        if(r.text != 'OK' ):
            print('try again', r.text)
            time.sleep(2)
        elif(r.text == 'OK' ):
            print('success', r.text)
            return
    list.append(1)
    return


@app.route('/batch-upload', methods=['POST'])
def index():
    threads = []
    list = []
    request = app.current_request
    array = request.json_body
    for file in array:
        x = threading.Thread(target=patch, args=(file, list))
        threads.append(x)
    for x in threads:
        x.start()
    # Wait for all of them to finish
    for x in threads:
        value = x.join()
    if (1 in list): raise ChaliceViewError('Error on update!')
    return {'message': 'OK'}



# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
