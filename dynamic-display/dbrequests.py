# coding: utf-8

import sys
import requests
import json
from bson.objectid import ObjectId

class dbrequests(object):

    @property
    def config_dict(self):
        return self._config_dict
    @config_dict.setter
    def config_dict(self, value):
        self._config_dict = value

    def search_user_in_list(self, user_id, list):
        for item in list:
            if item["user_id"] == user_id:
                return True
        return False

    def manual_encode(self, str):
        temp_encoded = str.replace("Ã©", 'é').replace("Ã§", 'ç').replace("Ã¨", 'è').replace("Ã«", 'ê').replace("Ãª", 'ê')
        encoded = temp_encoded.replace("Ã", 'à')
        return encoded

    def extract_numberlong(self, numberlong):
        number_string = json.dumps(numberlong)
        number = number_string.replace('{\"$numberLong\": \"', '').replace('\"}', '')
        return int(number.replace('\"', ''))

    def extract_objectid(self, oid):
        oid_string = json.dumps(oid)
        id = oid_string.replace('{\"$oid\": ', '').replace('}', '')
        return id.replace('\"', '')

    def get_fitcenter(self):
            fitcenter_dict = {}
            # TODO check connection availability
            with open("config/apiKey_license.txt") as file:  
                data = file.read()
                id = data
            try:
                result = requests.post(
                    "{}{}".format("http://91.121.155.83:5446/", "get/display/center"),
                    json=
                    {
                        'id': id
                    },
                    timeout=30)
                result.raise_for_status()
                fitcenter_json = result.json()
            except Exception as e: 
                print(e)
                return
            result_dict = result.json()
            fitcenter_dict["_id"] = self.extract_objectid(result_dict["_id"])
            fitcenter_dict["name"] = result_dict["name"]
            fitcenter_dict["city"] = result_dict["city"]
            return fitcenter_dict


    def get_configuration(self):
        self.config_dict = {} 
        fitcenter = self.get_fitcenter()
        try:
               result = requests.post(
                   "{}{}".format("http://91.121.155.83:5446/", "get/display/config"),
                   json=
                   {
                       'id': fitcenter["_id"]
                   },
                   timeout=30)
               result.raise_for_status()
        except Exception as e: 
            print(e)
            return
        result_dict = result.json()
        self.config_dict = result_dict.copy()
        self.config_dict["news_type"] = []
        for item in result_dict["news_type"]:
            self.config_dict["news_type"].append(item["value"])
        self.config_dict["_id"] = self.extract_objectid(result_dict["_id"])
        self.config_dict["fitness_center_id"] = self.extract_objectid(result_dict["fitness_center_id"])

    def get_events(self): #TODO TEST
        event_list = []
        if self.config_dict["show_events"] == True: #Should be initialize event is show_events False
         # for events in events_collection:
            for item in self.config_dict["selected_events"]:
                event_id = item["$oid"]
            try:
                result = requests.post(
                       "{}{}".format("http://91.121.155.83:5446/", "get/display/event"),
                    json=
                    {
                           'id': event_id
                    },
                    timeout=30,)
                result.raise_for_status()
            except Exception as e: 
                print(e)
                return
            result_dict = result.json()
            event_dict = {}
            event_dict["_id"] = self.extract_objectid(result_dict["_id"])
            event_dict["fitness_center_id"] = self.extract_objectid(result_dict["fitness_center_id"])
            event_dict["picture_id"] = self.extract_objectid(result_dict["fitness_center_id"])
            event_dict["pic"] = result_dict["picture"]
            event_dict["title"] = self.manual_encode(result_dict["title"])
            event_dict["description"] = self.manual_encode(result_dict["description"])
            event_dict["start_date"] = self.extract_numberlong(result_dict["start_date"])
            event_dict["end_date"] = self.extract_numberlong(result_dict["end_date"])
            event_list.append(event_dict)
        return event_list

    def get_user_pic(self, pic_id):
        try:
              result = requests.post(
                  "{}{}".format("http://91.121.155.83:5446/", "get/display/user/picture"),
                  json=
                  {
                      'id': pic_id
                  },
                  timeout=30)
              result.raise_for_status()
        except Exception as e: 
            print(e)
            return
        result_dict = result.json()
        return result_dict["picture"]
    
    def get_user(self, id):
        user_dict = {}
        try:
              result = requests.post(
                  "{}{}".format("http://91.121.155.83:5446/", "get/display/user"),
                  json=
                  {
                      'id': id
                  },
                  timeout=30)
              result.raise_for_status()
        except Exception as e: 
            print(e)
            return
        result_dict = result.json()
        user_dict["login"] = result_dict["login"]
        user_dict["pic"] = self.get_user_pic(self.extract_objectid(result_dict["picture_id"]))
        user_dict["fitness_center_id"] = self.extract_objectid(result_dict["fitness_center_id"])
        return user_dict

    def get_total_production_year(self):
        electric_productions = []
        total_production = 0
        fitcenter = self.get_fitcenter()
        try:
              result = requests.post(
                  "{}{}".format("http://91.121.155.83:5446/", "get/display/ppp"),
                  json=
                  {
                      'id': fitcenter["_id"]
                  },
                  timeout=30)
              result.raise_for_status()
        except Exception as e: 
            print(e)
            return 0
        result_array = result.json()
        for item in result_array:
            result_dict = json.loads(item)
            for electric_item in result_dict["electricproductions"]:
                total_production += electric_item["production_year"]
        return (total_production)
   
    def get_best_production_year(self):
        production_list = []
        electric_productions = []
        fitcenter = self.get_fitcenter()
        try:
              result = requests.post(
                  "{}{}".format("http://91.121.155.83:5446/", "get/display/ppp"),
                  json=
                  {
                      'id': fitcenter["_id"]
                  },
                  timeout=30)
              result.raise_for_status()
        except Exception as e: 
            print(e)
            return
        result_array = result.json()
        for item in result_array:
            result_dict = json.loads(item)
            for electric_item in result_dict["electricproductions"]:
                user_info = {}
                user_info = self.get_user(self.extract_objectid(electric_item["user_id"]))
                production_item = {}
                production_item["production_year"] = electric_item["production_year"]
                production_item["user_id"] = self.extract_objectid(electric_item["user_id"])
                production_item["user_login"] = user_info["login"]
                production_item["user_pic"] = user_info["pic"]
                electric_productions.append(production_item)
       
        for i in range(0, 3):  
            best_production = 0
            item = {}
            for j in range(len(electric_productions)):
                if electric_productions[j]["production_year"] > best_production:
                    if i > 0 :
                        if self.search_user_in_list(electric_productions[j]["user_id"], production_list) is True:
                            electric_productions[j]["production_day"] = 0
                            continue
                    best_production = electric_productions[j]["production_year"];
                    item = electric_productions[j]
            production_list.append(item)
            electric_productions.remove(item)
        return (production_list)
    
    def get_best_production_day(self):
        production_list = []
        electric_productions = []
        fitcenter = self.get_fitcenter()
        try:
              result = requests.post(
                  "{}{}".format("http://91.121.155.83:5446/", "get/display/ppp"),
                  json=
                  {
                      'id': fitcenter["_id"]
                  },
                  timeout=30)
              result.raise_for_status()
        except Exception as e: 
            print(e)
            return
        result_array = result.json()
        for item in result_array:
            result_dict = json.loads(item)
            for electric_item in result_dict["electricproductions"]:
                user_info = {}
                user_info = self.get_user(self.extract_objectid(electric_item["user_id"]))
                production_item = {}
                production_item["production_day"] = electric_item["production_day"]
                production_item["user_id"] = self.extract_objectid(electric_item["user_id"])
                production_item["user_login"] = user_info["login"]
                production_item["user_pic"] = user_info["pic"]
                electric_productions.append(production_item)
       
        for i in range(0, 3):  
            best_production = 0
            item = {}
            for j in range(len(electric_productions)):
                if electric_productions[j]["production_day"] > best_production:
                    if i > 0 :
                        if self.search_user_in_list(electric_productions[j]["user_id"], production_list) is True:
                            electric_productions[j]["production_day"] = 0
                            continue
                    best_production = electric_productions[j]["production_day"];
                    item = electric_productions[j]
            production_list.append(item)
            electric_productions.remove(item)

        return (production_list)