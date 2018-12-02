import sys
from pymongo import MongoClient
from bson.objectid import ObjectId
# pprint library is used to make the output look more pretty
from pprint import pprint


class dbconnector(object):
    # connection string from MongoDB server
    #_client = MongoClient('mongodb://centralefitness:Epitech42@91.121.155.83:27017/?connectTimeoutMS=2000')
    # connection string from SSH tunnel
    _client = MongoClient('mongodb://localhost:27017/?connectTimeoutMS=20000')
    _db = None
    _config_dict = {}


    @property
    def client(self):
        return self._client
    @client.setter
    def client(self, value):
        self._client = value

    @property
    def db(self):
        return self._db
    @db.setter
    def db(self, value):
        self._db = value

    @property
    def config_dict(self):
        return self._config_dict
    @config_dict.setter
    def config_dict(self, value):
        self._config_dict = value

    def __init__(self):
        self.db = self.client.centralefitness
        # Issue the serverStatus command and print the results
        try: self.db.command("serverStatus")
        except Exception as e: print(e) # TODO manage DB connection failure /!\
        else: print("Connection to the localhost database established")


    def db_close(self):
        self.client.close()


    def get_fitcenter_local(self):
        fitcenter_dict = {}
        fitcenter_dict["_id"] =  "Eden Fit"
        fitcenter_dict["city"] = "Marseille"
        return fitcenter_dict
         
    def get_fitcenter(self):
        fitcenter_dict = {}
        # TODO check connection availability
        collection = self.db.fitness_centers
        with open("config/fitness_center_id.txt") as file:  
            data = file.read()
            id = data
        centerquery = {"_id": ObjectId(id)}
        salle_collection = collection.find(centerquery)

         # Print all content of a doc
        for salle in salle_collection:
            fitcenter_dict["_id"] = salle["_id"]
            fitcenter_dict["name"] = salle["name"]
            fitcenter_dict["city"] = salle["city"]
        return fitcenter_dict

    def get_configuration_local(self):
        config_discipline = {}
        config_news = {}

        # Samples config
        config_discipline["ranking_discipline_type"] = ["running", "elliptique"]
        config_news["news_type"] = ["sport", "ecologie", "locale"] # If 'locale select city

        self.config_dict = {}
        self.config_dict["show_events"] = True
        self.config_dict["selected_events"] = "" # How get Array
        self.config_dict["show_global_performances"] = True # HallOfFame
        self.config_dict["show_ranking_discipline"] = True # should always be ON
        self.config_dict["ranking_discipline_type"] = config_discipline["ranking_discipline_type"] # scores of each discipline to display
        self.config_dict["show_global_ranking"] = False
        self.config_dict["show_national_production_ranking"] = False
        self.config_dict["show_news"] = True
        self.config_dict["news_type"] = "sport" # categories of rss news
   
       # Wait DB update
    def get_configuration(self):
        collection = self.db.display_configuration
        with open("config/fitness_center_id.txt") as file:  
            data = file.read()
            id = data
        if id:
            config_query = {"fitness_center_id" : ObjectId(id)}
            config_collection = collection.find(config_query)
            for config in config_collection:
                self.config_dict["show_events"] = config["show_events"]
                self.config_dict["selected_events"] = config["selected_events"]
                self.config_dict["show_global_performances"] = config["show_global_performances"]
                self.config_dict["show_ranking_discipline"] = config["show_ranking_discipline"]
                self.config_dict["ranking_discipline_type"] = config["ranking_discipline_type"]
                self.config_dict["show_global_ranking"] = config["show_global_ranking"]
                self.config_dict["show_national_production_rank"] = config["show_national_production_rank"]
                self.config_dict["show_news"] = config["show_news"]
                self.config_dict["news_type"] = []
                for item in config["news_type"]:
                    self.config_dict["news_type"].append(item["value"])
        else:
            print("Unable to load the fitness center id")

    def get_events_local(self):
        # should return a list of events {}
        event_dict = {}
        event_dict["title"] = "Retour de l'été"
        event_dict["description"] = "Profitez de l'été avec des séances de sport en plein air !"
        event_dict["pic"] = "style/img/park.png"
        return event_dict

    def get_events(self):
        event_list = []
        if self.config_dict["show_events"] == True: #Should be initialize event is show_events False
            collection = self.db.events
          #  event_dict["title"] = 
#            for events in events_collection:
            for item in self.config_dict["selected_events"]:
                events_query = {"_id" : item}
                events_collection = collection.find(events_query)
                for event in events_collection:
                    event_dict = {}
                    event_dict["title"] = event["title"]
                    event_dict["description"] = event["description"]
                    event_dict["pic"] = event["picture"]
                    event_dict["start_date"] = event["start_date"]
                    event_dict["end_date"] = event["end_date"]
                    print("event title : " + event["title"])
                    print("event desc : " + event["description"])
                    event_list.append(event_dict)
        return (event_list)

    def get_user_pic(self, pic_id):
        collection = self.db.pictures
        picture_query = {"_id" : ObjectId(pic_id)}
        picture_collection = collection.find(picture_query)
        for picture in picture_collection:
            return (picture["picture"])
    
    def get_user(self, id):
        user_dict = {}
        collection = self.db.users
        user_query = {"_id" : ObjectId(id)}
        users_collection = collection.find(user_query)
        for user in  users_collection:
            user_dict["login"] = user["login"]
            user_dict["pic"] = self.get_user_pic(user["picture_id"]) 
        return (user_dict)

    def get_best_production_year(self):
        production_list = []
        collection = self.db.electricproductions
        production_query = {}
        productions_collection = collection.find({})
        config_collection = collection.find(production_query).sort("production_year", -1).limit(3)
        for production in productions_collection:
            production_elem = {}
            user_info = {}
            user_info = self.get_user(production["user_id"])
            production_elem["production_year"] = production["production_year"]
            production_elem["user_login"] = user_info["login"]
            production_elem["user_pic"] = user_info["pic"]
            production_list.append(production_elem)
        return (production_list)

    def get_best_production_day(self):
        production_list = []
        collection = self.db.electricproductions
        production_query = {}
        productions_collection = collection.find({})
        config_collection = collection.find(production_query).sort("production_day", -1).limit(3)
        for production in productions_collection:
            production_elem = {}
            user_info = {}
            user_info = self.get_user(production["user_id"])
            production_elem["production_day"] = production["production_day"]
            production_elem["user_login"] = user_info["login"]
            production_elem["user_pic"] = user_info["pic"]
            production_list.append(production_elem)
        return (production_list)