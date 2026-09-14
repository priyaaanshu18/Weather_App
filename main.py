import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name : ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self) #Place Hodler
        self.emoji_label = QLabel(self) #Place Holder -> Delete them in a test run (used before)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self) :  #Initialized UI method
        self.setWindowTitle("Weather App")

        # Vertical Layout Manager -> To handle all the widgets
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        #vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.get_weather_button, alignment=Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("City_Label")
        self.city_input.setObjectName("City_Input")
        self.get_weather_button.setObjectName("Get_Weather_Button")
        self.temperature_label.setObjectName("Temperature_Label")
        self.emoji_label.setObjectName("Emoji_Label")
        self.description_label.setObjectName("Description_Label")

        self.setStyleSheet(""" 
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#City_Label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#City_Input{
                font-size: 40px;
            }
            QPushButton#Get_Weather_Button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#Temperature_Label{
                font-size: 75px;
            }
            QLabel#Emoji_Label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#Description_Label{
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)


    def get_weather(self) :
        api_key = "API_KEY_HERE"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try :
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200 :
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code :
                case 400 :
                    self.display_error("Bad Request :\nLook for your input")
                case 401 :
                    self.display_error("Unauthorized :\nInvalid API Key")
                case 403 :
                    self.display_error("Forbidden :\nAccess is denied")
                case 404 :
                    self.display_error("Not Found :\nCity not found")         
                case 500 :
                    self.display_error("Internal Server Error :\nPlease try again later")
                case 502 :
                    self.display_error("Bad Gateway :\nInvalid Response from the server")
                case 503 :
                    self.display_error("Service Unavailable :\nServer is down")
                case 504 :
                    self.display_error("Gateway Timeout :\nNo response from the server")
                case _ :
                    self.display_error(f"HTTP Error occured :\n{http_error}")                     

        except requests.exceptions.ConnectionError :
            self.display_error("Connection Error :\nCheck your internet connection")
        except requests.exceptions.Timeout :
            self.display_error("Timeout Error :\nThe request timed out")
        except requests.exceptions.TooManyRedirects :
            self.display_error("Too many redirects :\nCheck the URL")
        except requests.exceptions.RequestException as req_error :
            self.display_error(f"Request Error :\n{req_error}")


    def display_error(self,message) :
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data) :
        #print(data)
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15

        weather_id = data["weather"][0]["id"]

        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id) :
        if 200 <= weather_id <= 232 :
            return "⛈️"
        elif 300 <= weather_id <= 321 :
            return "☁️"
        elif 500<= weather_id <= 531 :
            return "🌧️"
        elif 600<= weather_id <= 632 :
            return "❄️"
        elif 701<= weather_id <= 741 :
            return "🌫️"
        elif weather_id == 762 :
            return "🌋"
        elif weather_id == 771 :
            return "💨"
        elif weather_id == 781 :
            return "🌪️"
        elif weather_id == 800 :
            return "☀️"
        elif 801 <= weather_id <= 804 :
            return "💭"
        else :
            return ""



if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
