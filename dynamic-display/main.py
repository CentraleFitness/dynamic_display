import sys
import json
import datetime

from time import strftime
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from rssfeeder import *
from dbconnector import *
from fitnesscenter import fitnesscenter
from utils import *

from sshtunnel import SSHTunnelForwarder

#SSH tunnel connection
SSH_HOST = "91.121.155.83"
SSH_USER = "centralefitness"
SSH_PASS = "Epitech42"

server = SSHTunnelForwarder(
    SSH_HOST,
    ssh_username=SSH_USER,
    ssh_password=SSH_PASS,
    remote_bind_address=('localhost', 27017),
    local_bind_address=('localhost', 27017)
)
try:
    server.start()
except Exception as e: 
    print(e)
    self.cf_db.db_close()
    self.close()
else: print("Creating SSH tunnel to the server " + SSH_HOST + "... OK")

screen_x = 0
screen_y = 0

class athlete(object):
    def __init__(self):
        self.name = "unknown"
        self.score = {'biking' : 0, 'running': 0, 'pulldown': 0, 'elliptique' : 0}
        self.picture = QtGui.QPixmap('style/img/user.png')

class MyWindow(QtWidgets.QMainWindow):
    _counter = 0
    _layout_counter = 0
    all_athlete = []
    _cf_db = dbconnector()
    now = QtCore.QDate.currentDate()
    timer = QtCore.QTimer()
    timer_info = QtCore.QTimer()

    @property
    def counter(self):
        return self._counter
    @counter.setter
    def counter(self, value):
        self._counter = value

    @property
    def layout_counter(self):
        return self._layout_counter
    @layout_counter.setter
    def layout_counter(self, value):
        self._layout_counter = value

    @property
    def cf_db(self):
        return self._cf_db

    def __init__(self):
        # Load the Ui
        super(MyWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)
        global screen_x
        global screen_y
        #self.setFixedSize(screen_x, screen_y)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        screenShape = QtWidgets.QDesktopWidget().screenGeometry()
        screen_x = screenShape.width()
        screen_y = screenShape.height()
        print("Screen size : x = " + str(screen_x) + ", y = " + str(screen_y))
        # Init DB connection
        # Init UI
        self.init_Ui()
        # used only with local config file, OR as long as there is no real users on DB
        self.get_json_data()
        self.cf_db.get_configuration()
        self.display_fitnesscenter()
        self.display_score()
        #self.display_events()
        self.display_rss()
        # Close DB connection
        #self.cf_db.db_close() NO DATA CONNECTION

    def init_Ui(self):
        # Load customed fonts
        self.fontDB = QtGui.QFontDatabase()
        self.fontDB.addApplicationFont("style/fonts/Aquawax Medium Trial.ttf")
        self.fontDB.addApplicationFont("style/fonts/LemonMilkitalic.otf")
        self.fontDB.addApplicationFont("style/fonts/Aquawax.otf")
        self.fontDB.addApplicationFont("style/fonts/built titling rg.ttf")
        self.fontDB.addApplicationFont("style/fonts/LemonMilk.otf")
        self.fontDB.addApplicationFont("style/fonts/LemonMilklight.otf")
        self.fontDB.addApplicationFont("style/fonts/DroidSans.ttf")

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget.setContentsMargins(20, 25, 20, 0)

        # Timer for refreshing infos, every 10 sec
        self.timer_info.timeout.connect(lambda: self.updateInfo())
        self.timer_info.start(10000)

        # Timer for refreshing display, every 15 sec
        self.timer.timeout.connect(lambda: self.update_all_contents())
        self.timer.start(15000)

        # Style the background
        self.refresher = QtCore.QTimer(self)

        # Create a gratient background
        p = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0, 0, screen_x, screen_y)
        gradient.setColorAt(0.0, QtGui.QColor(255, 189, 104))
        gradient.setColorAt(1.0, QtGui.QColor(255, 88, 137))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)

        # Display the date
        self.now.toString(QtCore.Qt.ISODate)
        now_date = self.now.toString('dd/MM/yyyy')
        self.date_time.setText(now_date)

        # Display the time
        self.timer_1_sec = QtCore.QTimer(self)
        self.timer_1_sec.timeout.connect(lambda: self.updateTime(now_date))
        self.timer_1_sec.start(1000)
        self.date_time.setText(now_date + "  " + strftime("%H"+":"+"%M"))
        self.date_time.setStyleSheet('color: white')
        self.date_time.setFont(QtGui.QFont("built titling rg", 20))

        # Center the title with a spacer
        self.header_layout.itemAt(2).changeSize((screen_x / 3) - (self.best_score.width() / 2), 20)

        self.best_score.setFont(QtGui.QFont("Aquawax", 20))
        self.best_score.setStyleSheet('color: white')

        # Add the logo as a footer
        pixmap = QtGui.QPixmap('style/img/LOGO_CF_WHITE.png')
        self.pic_label.setPixmap(pixmap.scaled(screen_x * 0.09, screen_y * 0.09, QtCore.Qt.KeepAspectRatio))

        self.show()

    def paintEvent(self, e):
        # Draw the news bar background
        line_news_y = self.line_news.y()
        line_footer_y = self.line_footer.y() + self.line_footer.height()
        line_height = line_footer_y - line_news_y

        painter = QtGui.QPainter(self)
        painter.setPen(Qt.white)
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        painter.drawRect(0, line_news_y, screen_x, line_height)


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
           self.cf_db.db_close()
           self.close()


    def get_json_data(self):
        with open("config/dynamic-display_config.json", "r") as json_data:
            data_dict = json.load(json_data)
        if "User1" in data_dict :
            athlete1 = createNewAthlete(data_dict["User1"])
            self.all_athlete.append(athlete1)
        if "User2" in data_dict :
            athlete2 = createNewAthlete(data_dict["User2"])
            self.all_athlete.append(athlete2)
        if "User3" in data_dict :
            athlete3 = createNewAthlete(data_dict["User3"])
            self.all_athlete.append(athlete3)
        if "User4" in data_dict :
            athlete4 = createNewAthlete(data_dict["User4"])
            self.all_athlete.append(athlete4)
        if "User5" in data_dict :
            athlete5 = createNewAthlete(data_dict["User5"])
            self.all_athlete.append(athlete5)
        if "User6" in data_dict :
            athlete6 = createNewAthlete(data_dict["User6"])
            self.all_athlete.append(athlete6)
        if "User7" in data_dict :
            athlete7 = createNewAthlete(data_dict["User7"])
            self.all_athlete.append(athlete7)
        if "User8" in data_dict :
            athlete8 = createNewAthlete(data_dict["User8"])
            self.all_athlete.append(athlete8)
        if "User9" in data_dict :
            athlete9 = createNewAthlete(data_dict["User9"])
            self.all_athlete.append(athlete9)
        if "User10" in data_dict :
            athlete10 = createNewAthlete(data_dict["User10"])
            self.all_athlete.append(athlete10)
        if "User11" in data_dict :
            athlete11 = createNewAthlete(data_dict["User11"])
            self.all_athlete.append(athlete11)
        if "User12" in data_dict :
            athlete12 = createNewAthlete(data_dict["User12"])
            self.all_athlete.append(athlete12)
        if "User13" in data_dict :
            athlete13 = createNewAthlete(data_dict["User13"])
            self.all_athlete.append(athlete13)
        if "User14" in data_dict :
            athlete14 = createNewAthlete(data_dict["User14"])
            self.all_athlete.append(athlete14)
        if "User15" in data_dict :
            athlete15 = createNewAthlete(data_dict["User15"])
            self.all_athlete.append(athlete15)


    def display_fitnesscenter(self):
         # Set the fitness center info
        fitcenter_dict = self.cf_db.get_fitcenter()
        myfitnesscenter = createFitnessCenter(fitcenter_dict)
        self.salle_name.setText(myfitnesscenter.name + "  " + myfitnesscenter.city)
        self.salle_name.setFont(QtGui.QFont("built titling rg", 20))
        self.salle_name.setStyleSheet('color: white')


    def display_score(self):
        # Should have all sport

        self.hall_of_fame = HallFameWidget(self, self.all_athlete)
        #shadow = QtGui.QGraphicsDropShadowEffect(self)
        #shadow.setBlurRadius(5)
        #self.hall_of_fame.setGraphicsEffect(shadow)

        self.scores_layout.setAlignment(QtCore.Qt.AlignLeft)

        #Only if get 1 sport
        #print("ranking type : " + self._cf_db.config_dict["ranking_discipline_type"])
        if self._cf_db.config_dict["ranking_discipline_type"] == "biking":
            self.sport_widget = DisciplineWidget_biking(self, self.all_athlete)
            self.scores_layout.addWidget(self.sport_widget)
        if self._cf_db.config_dict["ranking_discipline_type"] == "running":
            self.sport_widget2 = DisciplineWidget_running(self, self.all_athlete)
            self.scores_layout.addWidget(self.sport_widget2)
        if self._cf_db.config_dict["ranking_discipline_type"] == "pulldown":
            self.sport_widget3 = DisciplineWidget_pulldown(self, self.all_athlete)
            self.scores_layout.addWidget(self.sport_widget3)
        if self._cf_db.config_dict["ranking_discipline_type"] == "elliptic":
            self.sport_widget4 = DisciplineWidget_elliptique(self, self.all_athlete)
            self.scores_layout.addWidget(self.sport_widget4)

        self.updateScores()

        self.scores_layout.addWidget(self.hall_of_fame)


    def display_events(self):
        events = {}
        events_widgets = []
        if self.cf_db.config_dict["show_events"] == True:
            events = self.cf_db.get_events()
          
            # Multi events
            for event in events:
                event_widget = EventWidget(self, event)
                events_widgets.append(event_widget)
                self.scores_layout.setAlignment(QtCore.Qt.AlignCenter)
            for event in events_widgets:
                flag = 0
                items = (self.scores_layout.itemAt(i) for i in range(self.scores_layout.count()))
                for w in items:
                    if w.widget().objectName() == event.objectName():
                        flag = 1;
                        continue
                if flag == 0:
                    self.scores_layout.addWidget(event)
                

    def display_rss(self):
        if self.cf_db.config_dict["show_news"] == True:
            getRSSnews(allheadlines, self.cf_db.config_dict.get("news_type", None))
            news_widget = RSSWidget(self)
            self.news_layout.addWidget(news_widget)


    # SLOTS


    # Refresh time #fading asynchrone
    def updateTime(self, now_date):
        self.date_time.setText(now_date + " " + strftime("%H"+":"+"%M"))

    def update_all_contents(self):
        self.cf_db.get_configuration()
        layout_items = (self.scores_layout.itemAt(i) for i in range(self.scores_layout.count()))

        self.updateEvents()
        self.updateScores()

        items = (self.scores_layout.itemAt(i) for i in range(self.scores_layout.count()))
        for item in items:
            if item.widget().objectName() != "Form":
                if self.sport_widget4.isHidden() == False and self.hall_of_fame.isHidden() == False:
                     item.widget().show()
                elif self.sport_widget4.isHidden() == True and self.hall_of_fame.isHidden() == True:
                     item.widget().hide()
        if self.sport_widget4.isHidden() == False and self.hall_of_fame.isHidden() == False:
            #self.fade(self.sport_widget4)
            self.sport_widget4.hide()
            self.hall_of_fame.hide()
            #self.unfade(self.sport_widget4)
        elif self.sport_widget4.isHidden() == True and self.hall_of_fame.isHidden() == True:
            #self.fade(self.sport_widget4)
            self.sport_widget4.show()
            self.hall_of_fame.show()
            #self.unfade(self.sport_widget4)


    def updateInfo(self):
        if self._cf_db.config_dict["show_news"] == False:
            if self.news_layout.itemAt(0):
                self.news_layout.itemAt(0).widget().hide()
        else:
            if self.news_layout.itemAt(0).widget().isHidden():
                 self.news_layout.itemAt(0).widget().show()
            self.fade(self.news_layout.itemAt(0).widget().rss_info)
            print("updating infos, from pre-loaded buffer")
            if self.counter <= len(allheadlines):
                self.counter = self.counter + 1
            self.news_layout.itemAt(0).widget().rss_info.setText(allheadlines[self.counter]) #TODO IndexError when allheadlines empty
            self.unfade(self.news_layout.itemAt(0).widget().rss_info)

    def updateEvents(self):
        self.display_events()
       
                #if item.widget().isHidden() ==  False:
                    #self.fade(item.widget())
                    #item.widget().hide()
                #elif item.widget().isHidden() == True:
                    #item.widget().show()
                    #self.unfade(item.widget())

    def updateScores(self):
        print("updating score")
        user_discipline = []
        user_discipline = self.cf_db.get_best_production_day()

        # sport widget 4 is only for elliptic
        if self.sport_widget4:
            if user_discipline:
                self.sport_widget4.athlete_1_name.setText(user_discipline[0]["user_login"])
                self.sport_widget4.score_1.setText(str(round(user_discipline[0]["production_day"])) + " W")
            if len(user_discipline) > 1:
                self.sport_widget4.athlete_2_name.setText(user_discipline[1]["user_login"])
                self.sport_widget4.score_2.setText(str(round(user_discipline[1]["production_day"])) + " W")
            if len(user_discipline) > 2:
                self.sport_widget4.athlete_3_name.setText(user_discipline[2]["user_login"])
                self.sport_widget4.score_3.setText(str(round(user_discipline[2]["production_day"])) + " W")

        if self.hall_of_fame:
            users_hall_of_fame = []
            users_hall_of_fame = self.cf_db.get_best_production_year()
            if users_hall_of_fame:
                self.hall_of_fame.athlete_1.setText(users_hall_of_fame[0]["user_login"])
                pixmap_profile_1 = QtGui.QPixmap()
                if users_hall_of_fame[0]["user_pic"]:
                    pixmap_profile_1.loadFromData(get_data_from_uri(users_hall_of_fame[0]["user_pic"]))
                    self.hall_of_fame.athlete_1_pic.setPixmap(pixmap_profile_1.scaled(screen_x * 0.09, screen_y * 0.09, QtCore.Qt.KeepAspectRatio))
      
            if len(users_hall_of_fame) > 1:
                self.hall_of_fame.athlete_2.setText(users_hall_of_fame[1]["user_login"])
                pixmap_profile_2 = QtGui.QPixmap()
                if users_hall_of_fame[1]["user_pic"]:
                    pixmap_profile_2.loadFromData(get_data_from_uri(users_hall_of_fame[1]["user_pic"]))
                    self.hall_of_fame.athlete_2_pic.setPixmap(pixmap_profile_2.scaled(screen_x * 0.09, screen_y * 0.09, QtCore.Qt.KeepAspectRatio))

            if len(users_hall_of_fame) > 2:
                self.hall_of_fame.athlete_3.setText(users_hall_of_fame[2]["user_login"])
                pixmap_profile_3 = QtGui.QPixmap()
                if users_hall_of_fame[2]["user_pic"]:
                    pixmap_profile_3.loadFromData(get_data_from_uri(users_hall_of_fame[2]["user_pic"]))
                    self.hall_of_fame.athlete_3_pic.setPixmap(pixmap_profile_2.scaled(screen_x * 0.09, screen_y * 0.09, QtCore.Qt.KeepAspectRatio))


    def fade(self, widget):
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def unfade(self, widget):
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

def createFitnessCenter(fitcenter_dict):
    fitnesscenter_test = fitnesscenter()
    fitnesscenter_test.name = fitcenter_dict["name"]
    fitnesscenter_test.city = fitcenter_dict["city"]
    return fitnesscenter_test

def createNewAthlete(user_dict):
    athlete_test = athlete()
    athlete_test.name = user_dict["name"]
    athlete_test.picture = "style/img/" + user_dict["picture"]
    athlete_test.score = user_dict["score"]
    return athlete_test

allheadlines = []

#class FadedWidget(QtWidgets.QWidget):
#    def __init__(self, *args, **kwargs):
#        QtWidgets.QWidget.__init__(self, *args, **kwargs)
#        self.animation = QtCore.QVariantAnimation()
#        self.animation.valueChanged.connect(self.changeColor)

#class Widget1(QtWidgets.QWidget):
#    def __init__(self):
#        super().__init__()
#        lay = QtWidgets.QVBoxLayout(self)
#        greeting_text = QtWidgets.QLabel()
#        greeting_text.setStyleSheet("font : 45px; font : bold; font-family : HelveticaNeue-UltraLight")
#        greeting_text.setText("HELLO")
#        lay.addWidget(greeting_text)
#        #self.animation = QtCore.QVariantAnimation()
#        #self.animation.valueChanged.connect(self.changeColor)
#        ##btnFadeOut = QPushButton("fade out")
#        btnAnimation = QtWidgets.QPushButton("animation")
#        #lay.addWidget(btnFadeIn)
#        #lay.addWidget(btnFadeOut)
#        lay.addWidget(btnAnimation)
        
        #btnFadeIn.clicked.connect(self.greeting_text.startFadeIn)
        #btnFadeOut.clicked.connect(self.greeting_text.startFadeOut)
        #btnAnimation.clicked.connect(greeting_text.startAnimation)
        #timer_ = QtCore.QTimer(self)
        #timer_.timeout.connect(lambda: self.startAnimation())
        #timer_.start(10000)


class RSSWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(RSSWidget, self).__init__(parent)
        uic.loadUi('ui/RSSWidget.ui', self)

        pixmap = QtGui.QPixmap('style/img/news_4.png')
        self.news_pic.setPixmap(pixmap.scaled(screen_x * 0.08, screen_y * 0.08, QtCore.Qt.KeepAspectRatio))

        self.rss_info.setStyleSheet('color: #545454')
        self.rss_info.setFont(QtGui.QFont("Droid Sans", 16))
        self.rss_info.setText(allheadlines[0])



class EventWidget(QtWidgets.QWidget):
    def __init__(self, parent, event):
        super(EventWidget, self).__init__(parent)
        uic.loadUi('ui/EventWidget.ui', self)

        self.setObjectName("Event" + event["title"].replace(" ", ""))

        pic_data = get_data_from_uri(event["pic"])
        
        self.setStyleSheet('QLabel {color: white;} ')
        self.event_title.setText(event["title"])
        self.event_title.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.event_description.setText(event["description"])
        self.event_description.setFont(QtGui.QFont("Aquawax", 10))
        event_pic = QtGui.QPixmap()
        if not event_pic.loadFromData(pic_data):
            event_pic = QtGui.QPixmap('style/img/event.png')
        self.event_pic.setPixmap(event_pic.scaled(screen_x * 0.3, screen_y * 0.3, QtCore.Qt.KeepAspectRatio))
        startdate_to_display = datetime.datetime.fromtimestamp(event["start_date"]/1000.0)
        enddate_to_display = datetime.datetime.fromtimestamp(event["end_date"]/1000.0)
        self.event_date.setText("{:%d/%m/%Y}".format(startdate_to_display) + " - " + "{:%d/%m/%Y}".format(enddate_to_display))
        self.event_date.setFont(QtGui.QFont("Lemon/Milk", 10))

        self.hide()


class DisciplineWidget_biking(QtWidgets.QWidget):
    def __init__(self, parent, all_athlete):        
        super(DisciplineWidget_biking, self).__init__(parent)
        uic.loadUi('ui/DisciplineWidget_progress.ui', self)

        self.setStyleSheet('QLabel {color: white;} QProgressBar {border: 1px; text-align: center; padding: 1px; background: rgba(0, 0, 0, 0);} QProgressBar::chunk { background-color: white; }')

        self.progressBar_1.setTextVisible(False)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_3.setTextVisible(False)

        pixmap_sport = QtGui.QPixmap('style/img/biking.png')
        self.sport_pic.setPixmap(pixmap_sport.scaled(screen_x * 0.1, screen_y * 0.1, QtCore.Qt.KeepAspectRatio))

        self.sport_name.setText("Podium du jour en BIKING")
        self.sport_name.setFont(QtGui.QFont("Aquawax", 16))
        self.sport_name.setStyleSheet('color: white')

        self.score_1.setText(str(all_athlete[3].score["biking"]) + " W")
        self.score_1.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.score_2.setText(str(all_athlete[4].score["biking"]) + " W")
        self.score_2.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.score_3.setText(str(all_athlete[5].score["biking"]) + " W")
        self.score_3.setFont(QtGui.QFont("Lemon/Milk", 12))

        self.athlete_1_name.setText(all_athlete[3].name)
        self.athlete_1_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.setText(all_athlete[4].name)
        self.athlete_2_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.move(0, 20)
        self.athlete_3_name.setText(all_athlete[5].name)
        self.athlete_3_name.setFont(QtGui.QFont("Lemon/Milk", 9))

        self.show()


class DisciplineWidget_running(QtWidgets.QWidget):
    def __init__(self, parent, all_athlete):        
        super(DisciplineWidget_running, self).__init__(parent)
        uic.loadUi('ui/DisciplineWidget_progress.ui', self)

        self.setStyleSheet('QLabel {color: white;} QProgressBar {border: 1px; text-align: center; padding: 1px; background: rgba(0, 0, 0, 0);} QProgressBar::chunk { background-color: white; }')

        self.progressBar_1.setTextVisible(False)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_3.setTextVisible(False)

        pixmap_sport = QtGui.QPixmap('style/img/running.png')
        self.sport_pic.setPixmap(pixmap_sport.scaled(screen_x * 0.1, screen_y * 0.1, QtCore.Qt.KeepAspectRatio))

        self.sport_name.setText("Podium du jour en RUNNING")
        self.sport_name.setFont(QtGui.QFont("Aquawax", 16))
        self.sport_name.setStyleSheet('color: white')

        self.score_1.setText(str(all_athlete[6].score["running"]) + " W")
        self.score_1.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.score_2.setText(str(all_athlete[7].score["running"]) + " W")
        self.score_2.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.score_3.setText(str(all_athlete[8].score["running"]) + " W")
        self.score_3.setFont(QtGui.QFont("Lemon/Milk", 12))

        self.athlete_1_name.setText(all_athlete[6].name)
        self.athlete_1_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.setText(all_athlete[7].name)
        self.athlete_2_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.move(0, 20)
        self.athlete_3_name.setText(all_athlete[8].name)
        self.athlete_3_name.setFont(QtGui.QFont("Lemon/Milk", 9))

        self.progressBar_1.setValue(88)
        self.progressBar_2.setValue(78)
        self.progressBar_3.setValue(60)

        self.show()

class DisciplineWidget_pulldown(QtWidgets.QWidget):
    def __init__(self, parent, all_athlete):        
        super(DisciplineWidget_pulldown, self).__init__(parent)
        uic.loadUi('ui/DisciplineWidget_progress.ui', self)

        self.setStyleSheet('QLabel {color: white;} QProgressBar {border: 1px; text-align: center; padding: 1px; background: rgba(0, 0, 0, 0);} QProgressBar::chunk { background-color: white; }')

        self.progressBar_1.setTextVisible(False)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_3.setTextVisible(False)

        pixmap_sport = QtGui.QPixmap('style/img/pulldown.png')
        self.sport_pic.setPixmap(pixmap_sport.scaled(screen_x * 0.1, screen_y * 0.1, QtCore.Qt.KeepAspectRatio))

        self.sport_name.setText("Podium du jour en PULLDOWN")
        self.sport_name.setFont(QtGui.QFont("Aquawax", 16))
        self.sport_name.setStyleSheet('color: white')

        self.score_1.setText(str(all_athlete[9].score["pulldown"]) + " W")
        self.score_1.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_2.setText(str(all_athlete[10].score["pulldown"]) + " W")
        self.score_2.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_3.setText(str(all_athlete[11].score["pulldown"]) + " W")
        self.score_3.setFont(QtGui.QFont("Lemon/Milk", 9))

        self.athlete_1_name.setText(all_athlete[9].name)
        self.athlete_1_name.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.athlete_2_name.setText(all_athlete[10].name)
        self.athlete_2_name.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.athlete_2_name.move(0, 20)
        self.athlete_3_name.setText(all_athlete[11].name)
        self.athlete_3_name.setFont(QtGui.QFont("Lemon/Milk", 12))

        self.progressBar_1.setValue(88)
        self.progressBar_2.setValue(78)
        self.progressBar_3.setValue(60)

        self.show()

class DisciplineWidget_elliptique(QtWidgets.QWidget):
    def __init__(self, parent, all_athlete):        
        super(DisciplineWidget_elliptique, self).__init__(parent)
        uic.loadUi('ui/DisciplineWidget_progress.ui', self)

        self.setStyleSheet('QLabel {color: white;} QProgressBar {border: 1px; text-align: center; padding: 1px; background: rgba(0, 0, 0, 0);} QProgressBar::chunk { background-color: white; }')

        self.progressBar_1.setTextVisible(False)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_3.setTextVisible(False)

        pixmap_sport = QtGui.QPixmap('style/img/elliptique.png')
        self.sport_pic.setPixmap(pixmap_sport.scaled(screen_x * 0.1, screen_y * 0.1, QtCore.Qt.KeepAspectRatio))

        self.sport_name.setText("Podium du jour en ELLIPTIQUE")
        self.sport_name.setFont(QtGui.QFont("Aquawax", 16))
        self.sport_name.setStyleSheet('color: white')

        pixmap_trophy_1 = QtGui.QPixmap('style/img/trophy.png')
        self.trophy_1.setPixmap(pixmap_trophy_1.scaled(screen_x * 0.06, screen_y * 0.06, QtCore.Qt.KeepAspectRatio))
        pixmap_trophy_2 = QtGui.QPixmap('style/img/flags2.png')
        self.trophy_2.setPixmap(pixmap_trophy_2.scaled(screen_x * 0.06, screen_y * 0.06, QtCore.Qt.KeepAspectRatio))
        pixmap_trophy_3 = QtGui.QPixmap('style/img/flags3.png')
        self.trophy_3.setPixmap(pixmap_trophy_3.scaled(screen_x * 0.06, screen_y * 0.06, QtCore.Qt.KeepAspectRatio))

        self.score_1.setText(str(all_athlete[12].score["elliptique"]) + " W")
        self.score_1.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.score_2.setText(str(all_athlete[13].score["elliptique"]) + " W")
        self.score_2.setFont(QtGui.QFont("Lemon/Milk", 12))
        self.score_3.setText(str(all_athlete[14].score["elliptique"]) + " W")
        self.score_3.setFont(QtGui.QFont("Lemon/Milk", 12))

        self.athlete_1_name.setText(all_athlete[12].name)
        self.athlete_1_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.setText(all_athlete[13].name)
        self.athlete_2_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.move(0, 20)
        self.athlete_3_name.setText(all_athlete[14].name)
        self.athlete_3_name.setFont(QtGui.QFont("Lemon/Milk", 9))

        self.show()


class HallFameWidget(QtWidgets.QWidget):
    def __init__(self, parent, all_athlete):
        super(HallFameWidget, self).__init__(parent)
        uic.loadUi('ui/HallFameWidget.ui', self)

        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Background, QtGui.QColor(191, 132, 93))
        self.setPalette(p)
        
        self.setMaximumSize(screen_x / 3, screen_y) 

        pixmap_podium_1 = QtGui.QPixmap('style/img/trophy.png')
        self.podium_1.setPixmap(pixmap_podium_1.scaled(screen_x * 0.1, screen_y * 0.1, QtCore.Qt.KeepAspectRatio))
        pixmap_podium_2 = QtGui.QPixmap('style/img/flags2')
        self.podium_2.setPixmap(pixmap_podium_2.scaled(screen_x * 0.1, screen_y * 0.1, QtCore.Qt.KeepAspectRatio))
        pixmap_podium_3 = QtGui.QPixmap('style/img/flags3')
        self.podium_3.setPixmap(pixmap_podium_3.scaled(screen_x * 0.09, screen_y * 0.09, QtCore.Qt.KeepAspectRatio))

        self.athlete_1.setText(all_athlete[0].name)
        self.athlete_1.setFont(QtGui.QFont("Lemon/Milk light", 12))
        self.athlete_2.setText(all_athlete[14].name)
        self.athlete_2.setFont(QtGui.QFont("Lemon/Milk light", 12))
        self.athlete_3.setText(all_athlete[2].name)
        self.athlete_3.setFont(QtGui.QFont("Lemon/Milk light", 12))

        pixmap_profile_1 = QtGui.QPixmap('style/img/user.png')
        self.athlete_1_pic.setPixmap(pixmap_profile_1.scaled(screen_x * 0.2, screen_y * 0.2, QtCore.Qt.KeepAspectRatio))
        pixmap_profile_2 = QtGui.QPixmap('style/img/user.png')
        self.athlete_2_pic.setPixmap(pixmap_profile_2.scaled(screen_x * 0.2, screen_y * 0.2, QtCore.Qt.KeepAspectRatio))
        pixmap_profile_3 = QtGui.QPixmap('style/img/user.png')
        self.athlete_3_pic.setPixmap(pixmap_profile_3.scaled(screen_x * 0.2, screen_y * 0.2, QtCore.Qt.KeepAspectRatio))

        self.hall_of_fame.setFont(QtGui.QFont("Lemon/Milk", 20))
        self.description.setText("Meilleurs sportifs de l'année")
        self.description.setFont(QtGui.QFont("Aquawax", 15))

        self.show()

class ProductionWidget(QtWidgets.QWidget):
    def __init__(self, parent, all_athlete):
        super(HallFameWidget, self).__init__(parent)
        uic.loadUi('ui/ProductionWidget.ui', self)

        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setPalette(p)
        
        self.setMaximumSize(screen_x / 3, screen_y) 

        self.production.setText("C'est ce que vous produisez comme énergie!")
        self.production.setFont(QtGui.QFont("Lemon/Milk light", 12))

        production_picture = QtGui.QPixmap('style/img/electric.png')
        self.production_pic.setPixmap(production_picture.scaled(screen_x * 0.2, screen_y * 0.2, QtCore.Qt.KeepAspectRatio))

        self.title.setFont(QtGui.QFont("Lemon/Milk", 20))
        self.description.setFont(QtGui.QFont("Aquawax", 15))

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.all_athlete.clear()

     #Testing the Widget
    #DisciplineWidget = DisciplineWidget()

    #To load a generated Ui from code 
    #window = Qtwidgets.QMainWindow()
    #ui = ui_mainwindow()
    #ui.setupui(window)
    #window.show()

    sys.exit(app.exec_())
