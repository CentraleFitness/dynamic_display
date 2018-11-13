import sys
import json
import base64

from time import strftime
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets, uic
from rssfeeder import *
from dbconnector import *
from fitnesscenter import fitnesscenter

screen_x = 1920 * 2
screen_y = 1080 * 2
now = QtCore.QDate.currentDate()

class athlete(object):
    def __init__(self):
        self.name = "unknown"
        self.score = {'biking' : 0, 'running': 0, 'pulldown': 0, 'elliptique' : 0}
        self.picture = QtGui.QPixmap('style/img/user.png')

class MyWindow(QtWidgets.QMainWindow):
    _counter = 0
    all_athlete = []
    _cf_db = dbconnector()
    keyPressed = QtCore.pyqtSignal(int)

    @property
    def counter(self):
        return self._counter
    @counter.setter
    def counter(self, value):
        self._counter = value

    @property
    def cf_db(self):
        return self._cf_db

    def __init__(self):
        # Load the Ui
        super(MyWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)
        self.setFixedSize(screen_x, screen_y)

        # Init DB connection
       # self.cf_db = dbconnector() #NO DATA CONNECTION
        # Init UI
        self.init_Ui()
        # used only with local config file, OR as long as there is no real users on DB
        self.get_json_data()
        self.cf_db.get_configuration()
        self.display_fitnesscenter()
        self.display_score()
        self.display_events()
        self.display_rss()
        self.keyPressed.connect(self.on_key)
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

        # Style the background
        self.refresher = QtCore.QTimer(self)

        #self.refresher.timeout.connect(self.)

        #Style the background with video
        #player = QtMultimedia.QMediaPlayer      
        #vw = QtMultimediaWidgets.QVideoWidget
        #player.setVideoOutput(vw)
        #player.setMedia(QtCore.QUrl.fromLocalFile("style/background_sample.mov"))
        #vw.setGeometry(100, 100, 300, 400)
        #vw.show()
        #player.play()
        #qDebug() << player.state()

        # Create a gratient background
        p = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0, 0, screen_x, screen_y)
        gradient.setColorAt(0.0, QtGui.QColor(255, 189, 104))
        gradient.setColorAt(1.0, QtGui.QColor(255, 88, 137))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)

        # Display the date
        now.toString(QtCore.Qt.ISODate)
        now_date = now.toString('dd/MM/yyyy')
        self.date_time.setText(now_date)

        # Display the time
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.updateTime(now_date))
        self.timer.start(1000)
        self.date_time.setText(now_date + "  " + strftime("%H"+":"+"%M"))
        self.date_time.setStyleSheet('color: white')
        self.date_time.setFont(QtGui.QFont("built titling rg", 14))

        # Center the title with a spacer
        self.header_layout.itemAt(2).changeSize((screen_x / 3) - (self.best_score.width() / 2), 20)

        self.best_score.setFont(QtGui.QFont("Aquawax", 20))
        self.best_score.setStyleSheet('color: white')

        # Add the logo as a footer
        pixmap = QtGui.QPixmap('style/img/LOGO_CF_WHITE.png')
        self.pic_label.setPixmap(pixmap.scaled(screen_x * 0.08, screen_y * 0.08, QtCore.Qt.KeepAspectRatio))

        # Add a signal when "Escape" in pressed
        #keyPressed = QtCore.pyqtSignal(int)

        self.show()

    def keyPressEvent(self, event):
        super(MyWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event)

    def on_key(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            quit()
            #self.close()
    

    def get_json_data(self):
        with open("config/dynamic-display_config.json", "r") as json_data:
            data_dict = json.load(json_data)
        #if "FitnesscenterName" and "FitnesscenterAdress" in data_dict :
        #    self.salle_name.setText(data_dict["FitnesscenterName"] + " " + data_dict["FitnesscenterAdress"])
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
#        fitcenter_dict = {"name": "Eden Fit", "city": "Marseille"}
        myfitnesscenter = createFitnessCenter(fitcenter_dict)
        self.salle_name.setText(myfitnesscenter.name + "  " + myfitnesscenter.city)
        self.salle_name.setFont(QtGui.QFont("built titling rg", 14))
        self.salle_name.setStyleSheet('color: white')


    def display_score(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateScores)
        self.timer.start(15000)
        # Should have all sport
        #self.sport_widget = DisciplineWidget_biking(self, self.all_athlete)
        #self.sport_widget2 = DisciplineWidget_running(self, self.all_athlete)
        #self.sport_widget3 = DisciplineWidget_pulldown(self, self.all_athlete)
        #self.sport_widget4 = DisciplineWidget_elliptique(self, self.all_athlete)

       # self.hall_of_fame = HallFameWidget(self, self.all_athlete)
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

         # Should have all sports
        #self.scores_layout.addWidget(self.sport_widget)
        #self.scores_layout.addWidget(self.sport_widget2)
        #self.scores_layout.addWidget(self.sport_widget3)
        #self.scores_layout.addWidget(self.sport_widget4)

        #self.sport_widget3.hide()
        #self.sport_widget4.hide()

        #self.scores_layout.addWidget(self.hall_of_fame)


    def display_events(self):
        events = {}
        events_widgets = []
        if self.cf_db.config_dict["show_events"] == True:
            events = self.cf_db.get_events()
          # Only 1
           # event_widget = EventWidget(self, events[0])
            #self.scores_layout.addWidget(event_widget)
          
            # Multi events
            for event in events:
                event_widget = EventWidget(self, event)
                events_widgets.append(event_widget)
            for event in events_widgets:
                self.scores_layout.addWidget(event)

    def display_rss(self):
        if self.cf_db.config_dict["show_news"] == True:
            print(self.cf_db.config_dict["news_type"])
            getRSSnews(allheadlines, self.cf_db.config_dict.get("news_type", None))
            pixmap = QtGui.QPixmap('style/img/news.png')
            self.news_pic.setPixmap(pixmap.scaled(screen_x * 0.06, screen_y * 0.06, QtCore.Qt.KeepAspectRatio))
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(lambda: self.updateInfo(self.counter))
            self.timer.start(15000)
            self.rss_info.setText(allheadlines[0])
            self.rss_info.setStyleSheet('color: white')
            self.rss_info.setFont(QtGui.QFont("Droid Sans", 12))


    # SLOTS


    # Refresh time
    def updateTime(self, now_date):
        self.date_time.setText(now_date + " " + strftime("%H"+":"+"%M"))

    def updateInfo(self, index):
        if self.counter <= len(allheadlines):
            self.counter = self.counter + 1
        self.rss_info.setText(allheadlines[self.counter]) #TODO IndexError when allheadlines empty

    def updateScores(self):
        print("hello")
        #if self.sport_widget3.isHidden and self.sport_widget4.isHidden:
        #    self.sport_widget.hide()
        #    self.sport_widget2.hide()
        #    self.sport_widget3.show()
        #    self.sport_widget4.show()
        #    self.sport_widget3.isHidden = False
        #    self.sport_widget4.isHidden = False
        #else:
        #    self.sport_widget3.hide()
        #    self.sport_widget4.hide()
        #    self.sport_widget.show()
        #    self.sport_widget2.show()
        #    self.sport_widget3.isHidden = True
        #    self.sport_widget4.isHidden = True
 
    def unfaded(self):
        self.rss_info

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


class EventWidget(QtWidgets.QWidget):
    def __init__(self, parent, event):
        super(EventWidget, self).__init__(parent)
        uic.loadUi('ui/EventWidget.ui', self)

     #   pic_recovered = base64.decodestring(event["pic"])
      #  pic_file = event["title"].split(' ', 1)[0]
       # print("PIC NAME : " + pic_file)
        #f = open("")
        self.setStyleSheet('QLabel {color: white;} ')
        self.event_title.setText(event["title"])
        self.event_title.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.event_description.setText(event["description"])
        self.event_description.setFont(QtGui.QFont("Aquawax", 8))
        if event["title"] == "Retour de l'été":
            event_pic = QtGui.QPixmap('style/img/park.png')
        else:
            event_pic = QtGui.QPixmap('style/img/event.png')
        self.event_pic.setPixmap(event_pic.scaled(screen_x * 0.2, screen_y * 0.2, QtCore.Qt.KeepAspectRatio))


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

        self.sport_name.setText("BIKING")
        self.sport_name.setFont(QtGui.QFont("Aquawax", 18))
        self.sport_name.setStyleSheet('color: white')

        self.score_1.setText(str(all_athlete[3].score["biking"]) + " W")
        self.score_1.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_2.setText(str(all_athlete[4].score["biking"]) + " W")
        self.score_2.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_3.setText(str(all_athlete[5].score["biking"]) + " W")
        self.score_3.setFont(QtGui.QFont("Lemon/Milk", 9))

        self.athlete_1_name.setText(all_athlete[3].name)
        self.athlete_1_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.setText(all_athlete[4].name)
        self.athlete_2_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.move(0, 20)
        self.athlete_3_name.setText(all_athlete[5].name)
        self.athlete_3_name.setFont(QtGui.QFont("Lemon/Milk", 9))

        #self.timerAnimation = QtCore.QTimer(self)

        #opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        #self.setGraphicsEffect(opacityEffect)
        #opacityEffect.setOpacity(1)

        #rssAnimation = QtCore.QPropertyAnimation(opacityEffect, b"opacity")
        #rssAnimation.setStartValue(1)
        #rssAnimation.setEndValue(0)
        #rssAnimation.setDuration(2000)
        #rssAnimation.setEasingCurve(QtCore.QEasingCurve.Linear)
        #rssAnimation.valueChanged.connect(self.unfaded)

        #self.timerAnimation.timeout.connect(self.faded)
        #self.timerAnimation.start(13000)

        self.show()

    #def faded(self):
    #    #self.rss_info
    #    self.rssAnimation.start()

    #def unfaded(self):
    #    if self.rssAnimation.direction == QtCore.QAbstractAnimation.Forward:
    #        self.rssAnimation.setDirection(QtCore.QAbstractAnimation.Backward)
    #    else:
    #        self.rssAnimation.setDirection(QtCore.AbstractAnimation.Forward)

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

        self.sport_name.setText("RUNNING")
        self.sport_name.setFont(QtGui.QFont("Aquawax", 18))
        self.sport_name.setStyleSheet('color: white')

        self.score_1.setText(str(all_athlete[6].score["running"]) + " W")
        self.score_1.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_2.setText(str(all_athlete[7].score["running"]) + " W")
        self.score_2.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_3.setText(str(all_athlete[8].score["running"]) + " W")
        self.score_3.setFont(QtGui.QFont("Lemon/Milk", 9))

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

        self.sport_name.setText("PULLDOWN")
        self.sport_name.setFont(QtGui.QFont("Aquawax", 18))
        self.sport_name.setStyleSheet('color: white')

        self.score_1.setText(str(all_athlete[9].score["pulldown"]) + " W")
        self.score_1.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_2.setText(str(all_athlete[10].score["pulldown"]) + " W")
        self.score_2.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_3.setText(str(all_athlete[11].score["pulldown"]) + " W")
        self.score_3.setFont(QtGui.QFont("Lemon/Milk", 9))

        self.athlete_1_name.setText(all_athlete[9].name)
        self.athlete_1_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.setText(all_athlete[10].name)
        self.athlete_2_name.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.athlete_2_name.move(0, 20)
        self.athlete_3_name.setText(all_athlete[11].name)
        self.athlete_3_name.setFont(QtGui.QFont("Lemon/Milk", 9))

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

        self.sport_name.setText("ELLIPTIQUE")
        self.sport_name.setFont(QtGui.QFont("Aquawax", 18))
        self.sport_name.setStyleSheet('color: white')

        self.score_1.setText(str(all_athlete[12].score["elliptique"]) + " W")
        self.score_1.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_2.setText(str(all_athlete[13].score["elliptique"]) + " W")
        self.score_2.setFont(QtGui.QFont("Lemon/Milk", 9))
        self.score_3.setText(str(all_athlete[14].score["elliptique"]) + " W")
        self.score_3.setFont(QtGui.QFont("Lemon/Milk", 9))

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

        pixmap_profile_1 = QtGui.QPixmap('style/img/athlete_1.png')
        self.athlete_1_pic.setPixmap(pixmap_profile_1.scaledToWidth(80))
        pixmap_profile_2 = QtGui.QPixmap('style/img/athlete_2.png')
        self.athlete_2_pic.setPixmap(pixmap_profile_2.scaledToWidth(80))
        pixmap_profile_3 = QtGui.QPixmap('style/img/athlete_3.png')
        self.athlete_3_pic.setPixmap(pixmap_profile_3.scaledToWidth(80))

        self.hall_of_fame.setFont(QtGui.QFont("Lemon/Milk", 16))

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.all_athlete.clear()

     #Testing the Widget
    #DisciplineWidget = DisciplineWidget()

    #To load a generated Ui from code 
    #window = QtWidgets.QMainWindow()
    #ui = Ui_MainWindow()
    #ui.setupUi(window)
    #window.show()

    sys.exit(app.exec_())