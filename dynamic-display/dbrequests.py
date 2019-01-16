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
            event_dict = result_dict.copy()
            event_dict["_id"] = self.extract_objectid(result_dict["_id"])
            event_dict["fitness_center_id"] = self.extract_objectid(result_dict["fitness_center_id"])
            event_dict["picture_id"] = self.extract_objectid(result_dict["fitness_center_id"])
            #description = result_dict["description"]
            # TODO ENCODING
            #event_dict["description"] = description.decode("utf-8")
            event_list.append(event_dict)
        return event_list

    def get_user_pic(self, pic_id):
        return picture["picture"]
    
    def get_user(self, id):
        user_dict = {}
        return user_dict

    def get_total_production_year(self):
        production_list = []
        return (production_list)

    def get_best_production_year(self):
        production_list = []
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
                electric_productions.append(electric_item)
       
        for i in range(0, 3):  
            best_production = 0
            for item in electric_productions:      
                if item["production_day"] > best_production: 
                    best_production = item["production_day"]
            production_list.append(item)
            electric_productions.remove(item)

        print(production_list) 
        return (production_list)