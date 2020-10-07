import json
import requests

community_specific_schema = "38adc6cc-e716-4c9e-8169-c82a557812e1";
headers = {"Content-Type": "application/json"};
headers_patch = {"Content-Type": "application/json-patch+json"};
token = "your_token";
metadata = [{"op": "add", "path":"/publication_state", "value": "submitted"}];

def publish_dataset(id):
    url = "https://eudat-b2share-test.csc.fi/api/records/" + id + "/draft?access_token=" + token;
    r = requests.patch(url, data=json.dumps(metadata), headers=headers_patch);

def get_id(name):
    url = "https://eudat-b2share-test.csc.fi/api/records/?drafts&access_token=" + token+"&q=titles.title:"+name;
    r = requests.get(url);
    print(name+" - "+r.json()["hits"]["hits"][0]["id"]);
    publish_dataset(r.json()["hits"]["hits"][0]["id"]);

def load_interval(begin, end):
    with open('photometers3.json') as json_file:
        data = json.load(json_file);
        for photometer in data:
            tess_number = photometer['name'][5:]
            if (int(tess_number)>=begin) and (int (tess_number)<=end):
                try:
                    get_id(photometer["name"]);
                except:
                    print("Dataset not present");

load_interval(201,400);