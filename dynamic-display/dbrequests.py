import sys
import requests
from bson.objectid import ObjectId

class dbrequests(object):

    @property
    def config_dict(self):
        return self._config_dict
    @config_dict.setter
    def config_dict(self, value):
        self._config_dict = value


    def get_fitcenter(self):
            fitcenter_dict = {}
            # TODO check connection availability
            with open("config/apiKey_license.txt") as file:  
                data = file.read()
                id = data
            # DEBUG WAIT FOR APIKEY ROUTE
            #id = "5bf72d7efb56e5539cb102ee" apiKey
            id = "5c08768810dc325cfbac8769" # id
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
            fitcenter_dict["_id"] = result_dict["_id"]
            fitcenter_dict["name"] = result_dict["name"]
            fitcenter_dict["city"] = result_dict["city"]
            return fitcenter_dict


    def get_configuration(self):
        self.config_dict = {} 
        #fitcenter = self.get_fitcenter() WAIT FOR APIKEY ROUTE
        # DEBUG
        fitcenter = "5c08768810dc325cfbac8769"

        try:
               result = requests.post(
                   "{}{}".format("http://91.121.155.83:5446/", "get/display/config"),
                   json=
                   {
                       'id': fitcenter
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
        print(self.config_dict["news_type"])

    def get_events(self):
        event_list = []
        if self.config_dict["show_events"] == True: #Should be initialize event is show_events False
         # for events in events_collection:
            for item in self.config_dict["selected_events"]:
                event_id = {"_id" : item}
            try:
                result = requests.post(
                       "{}{}".format("http://91.121.155.83:5446/", "get/display/event"),
                    json=
                    {
                           'id': event_id
                    },
                    timeout=30)
                result.raise_for_status()
            except Exception as e: 
                print(e)
                return
            result_dict = result.json()
            event_list.append(result_dict)
        return event_list