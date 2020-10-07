import json
import requests

community_specific_schema = "38adc6cc-e716-4c9e-8169-c82a557812e1";
headers = {"Content-Type": "application/json"};
token = "your_token";

metadata_record = {
  "titles": [
    {
      "title": "test28"
    }
  ],
  "creators": [
    {
      "creator_name": "STARS4ALL"
    }
  ],
  "descriptions": [
    {
      "description": "Measurements taken from the STARS4ALL network (http://tess.stars4all.eu)",
      "description_type": "Abstract"
    }
  ],
  "license":
      {
        "license": "Creative Commons Attribution-ShareAlike (CC-BY-SA)",
        "license_uri": "http://creativecommons.org/licenses/by-sa/4.0/"
      },
  "keywords": ["photometers","light_pollution","measurements","skyglow","pollution"],
  "resource_types":[
      {
        "resource_type": "Incremental dataset",
        "resource_type_general": "Dataset"
      }
  ],
  "version": "1",
  "publisher": "STARS4ALL",
  "contact_email": "stars4all@gmail.com",
  "community": "630291ac-db47-48bf-b8aa-7acdb482c430",
  "community_specific": {
    "38adc6cc-e716-4c9e-8169-c82a557812e1": {
      "cover_offset_value": 20,
      "creative_work_type": "Dataset",
      "device_type": "TESS-W",
      "field_of_view": 10,
      "filters_per_channel": [1],
      "firmware_version": "1.0",
      "instrument_id": "stars26",
      "local_timezone":"UTC+1",
      "look_direction": "Fixed",
      "mac_address": "18:FE:34:CF:E9:A3",
      "measurement_direction_per_channel": [90],
      "number_of_channels": 1,
      "position": "Fixed",
      "source": "Sensor",
      "standard": "SKYGLOW DEFINITIONS 1.0",
      "standard_url": "http://www.darksky.org/NSBM/sdf1.0.pdf",
      "supplier": "STARS4ALL",
      "zero_point": 20.5
    }
  },
  "open_access": True,
}


def load_interval(begin, end):
    with open('photometers3.json') as json_file:
        data = json.load(json_file);
        for photometer in data:
            tess_number = photometer['name'][5:]
            if (int(tess_number)>=begin) and (int (tess_number)<=end):
                create_metadata(photometer);
                #print(photometer)
                #print(tess_number)

def create_metadata(photometer):
    title = metadata_record["titles"][0]["title"];

    metadata_record["titles"][0]["title"]=photometer["name"];
    metadata_record["community_specific"][community_specific_schema]["instrument_id"]=photometer["name"];
    try:
        metadata_record["community_specific"][community_specific_schema]["local_timezone"]=photometer["info_tess"]["local_timezone"];
    except:
        print("Error in local_timezone");
    #metadata_record["community_specific"][community_specific_schema]["local_timezone"] = photometer["local_timezone"];
    metadata_record["community_specific"][community_specific_schema]["mac_address"]=photometer["mac"];
    try:
        metadata_record["community_specific"][community_specific_schema]["zero_point"]=photometer["info_tess"]["zero_point"];
    except:
        print("Error in zero_point");
    url = "https://eudat-b2share-test.csc.fi/api/records/?access_token=" + token;
    params = {'access_token': token}
    r = requests.post(url, json=metadata_record, headers=headers);

    print(photometer["name"]+","+r.json()["id"]+","+str(r.status_code));

    upload_file(photometer["name"],r.json()["links"]["files"]);

def upload_file(name,fileid):
    headers_upload = {"Content-Type": "application/octet-stream", "Slug": "stars4all-"+name+".csv"};
    url = fileid+"/stars4all-"+name+"?access_token=" + token;
    file_name = "./datasets/stars4all-"+name+".csv";

    try:
        r = requests.put(url, data=open(file_name, 'rb'), headers=headers_upload);
    except:
        print("Existint identifier");


load_interval(201,400);