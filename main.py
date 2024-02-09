from PyQt5 import QtCore, QtGui, QtWidgets
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pywhatkit
import wikipedia
import pyjokes
import pyautogui
import sys
import subprocess


recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)


class WorkerThread(QtCore.QThread):
    reactorSignal = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.reactorSignal.emit()
            self.msleep(300)


class SpeechRecognitionThread(QtCore.QThread):
    speechRecognitionSignal = QtCore.pyqtSignal(str)

    def run(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("Say something:")
                    audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                text = text.lower()
                print("You asked:", text)
                self.speechRecognitionSignal.emit(text)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Could not request result from Google Speech Recognition service. {e}")
                pass


class Ui_mainGUI(object):
    def setupUi(self, mainGUI):
        mainGUI.setObjectName("mainGUI")
        mainGUI.resize(600, 800)
        mainGUI.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.reactor = QtWidgets.QLabel(mainGUI)
        self.reactor.setGeometry(QtCore.QRect(10, 110, 571, 421))
        self.reactor.setText("")
        self.reactor.setScaledContents(True)
        self.reactor.setObjectName("reactor")
        self.jarvis = QtWidgets.QLabel(mainGUI)
        self.jarvis.setGeometry(QtCore.QRect(40, 10, 511, 101))
        self.jarvis.setText("")
        self.jarvis.setPixmap(QtGui.QPixmap("D:/jarvis-virtual assistant/gui-gifs/attachment_97425804 (1).jpeg"))
        self.jarvis.setScaledContents(True)
        self.jarvis.setObjectName("jarvis")
        self.output = QtWidgets.QPlainTextEdit(mainGUI)
        self.output.setGeometry(QtCore.QRect(10, 540, 581, 251))
        self.output.setPlainText("")
        self.output.setObjectName("output")

        self.retranslateUi(mainGUI)
        QtCore.QMetaObject.connectSlotsByName(mainGUI)

    def retranslateUi(self, mainGUI):
        _translate = QtCore.QCoreApplication.translate
        mainGUI.setWindowTitle(_translate("mainGUI", "mainGUI"))


class Jarvis(QtWidgets.QWidget):
    def __init__(self):
        super(Jarvis, self).__init__()

        self.ui = Ui_mainGUI()
        self.ui.setupUi(self)
        self.greeting()

        self.ui.output.setStyleSheet("color: white;")

        self.ui.reactor.movie = QtGui.QMovie("D:/jarvis-virtual assistant/gui-gifs/SVKl.gif")
        self.ui.reactor.movie.setSpeed(250)
        self.ui.reactor.setMovie(self.ui.reactor.movie)

        self.reactor_thread = WorkerThread()
        self.reactor_thread.reactorSignal.connect(self.show_reactor_gui)
        self.reactor_thread.start()

        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.speechRecognitionSignal.connect(self.handle_speech)
        self.speech_thread.start()

    def greeting(self):
        time = datetime.datetime.now().hour
        if 0 <= time < 12:
            self.talk("good morning,sir")

        elif 12 < time <= 15:
            self.talk("good afternoon,sir")
        else:
            self.talk("good evening,sir")
        self.talk("I'm Jarvis, your virtual assistant. How can I help you?")

    def talk(self, text):
        self.ui.output.appendPlainText(text)
        engine.say(text)
        engine.runAndWait()

    def handle_speech(self, text):
        self.show_reactor_gui()
        command = text
        if "search" in command:
            command = command.replace("jarvis", "")
            query = command.replace("search", "").strip()
            self.talk("result based on search")
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)

        elif "play" in command:
            command = command.replace("jarvis", "")
            song = command.replace("play", "")
            self.talk("playing" + song)
            pywhatkit.playonyt(song)

        elif "how are you" in command:
            self.talk("I'm doing well, thanks for asking, sir!")

        elif "who are you" in command:
            self.talk("I'm Jarvis, your virtual assistant.")

        elif "who created you" in command:
            self.talk("I was created by Mr. Ahmed.")

        elif "what's your job" in command:
            self.talk("I'll assist you, sir.")

        elif "turn on wi-fi" in command:
            self.talk("turning on wi-fi sir")
            subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"])

        elif "turn off wi-fi" in command:
            self.talk("turning off wi-fi sir")
            subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "disabled"])

        elif "go to sleep" in command:
            print("It's good to assist you, sir. Call me whenever you need.")
            self.talk("It's good to assist you, sir. Call me whenever you need.")
            exit()

        elif "time now" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            print(time)
            self.talk("It's " + time + " now, sir.")

        elif "joke" in command:
            self.talk(pyjokes.get_joke())

        elif "open" in command:
            pyautogui.press('super')
            pyautogui.press('Cortana Search')
            command = command.replace("jarvis", "")
            command = command.replace("open", "")
            pyautogui.typewrite(command)
            pyautogui.sleep(1)
            pyautogui.press("enter")
            self.talk("Opening sir.")

        elif "close" in command:
            self.talk("Closing sir")
            pyautogui.hotkey('alt', 'f4')

        elif "what" in command or "who" in command:
            detail = command.replace("what", "").replace("who", "")
            try:
                info = wikipedia.summary(detail, 1)
                self.talk(info)
            except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError) as e:
                if isinstance(e, wikipedia.exceptions.DisambiguationError):
                    self.talk("Multiple options found. Please provide a more specific query.")
                else:
                    self.talk(f"Sorry, I couldn't find information on '{command}'. Can you ask something else?")
            except Exception as e:
                self.talk(f"An error occurred: {str(e)}. Please try again.")

        else:
            self.talk("Sorry, I don't understand")

        self.pause_reactor_gui()

    def show_reactor_gui(self):
        self.ui.reactor.movie.stop()
        self.ui.reactor.movie.start()
        self.ui.reactor.show()

    def pause_reactor_gui(self):
        self.ui.reactor.movie.stop()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    main_window = QtWidgets.QMainWindow()
    ui = Ui_mainGUI()
    ui.setupUi(main_window)
    main_window.show()

    jarvis_app = Jarvis()
    jarvis_app.setParent(main_window)
    jarvis_app.show()

    sys.exit(app.exec_())
