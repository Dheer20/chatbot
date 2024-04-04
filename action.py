import datetime
import webbrowser
import requests
import wikipedia
import pyttsx3
import time
from requests_html import HTMLSession

class Action:
    def __init__(self, user_input):
        self.user_input = user_input
        

    def handle_action(self):

         
        if "what is your name" in self.user_input:
          self.text_to_speech("My name is virtual assistant")
          return "My name is virtual assistant"

        elif "hello" in self.user_input or "hi" in self.user_input:
          self.text_to_speech("Hey, sir. How can I help you?")
          return "Hey, sir. How can I help you?"

        elif "search" in self.user_input:  # Example trigger for API search
          query = self.user_input.replace("search", "").strip()
          api_response = self.search_api(query)
          self.text_to_speech(api_response)
          return api_response
        
        elif "good morning" in self.user_input:
          self.text_to_speech("Good morning, sir")
          return "Good morning, sir"
        
        elif "time now" in self.user_input:
          current_time = datetime.datetime.now()
          time_str = f"Hour: {current_time.hour}, Minute: {current_time.minute}"
          self.text_to_speech(time_str)
          return time_str

        elif "shutdown" in self.user_input:
          return "Ok sir"

        elif "play music" in self.user_input:
          webbrowser.open("https://open.spotify.com/")
          self.text_to_speech("Opening Spotify, enjoy your songs")
          return "Opening Spotify, enjoy your songs"

        elif "play YouTube" in self.user_input:
          webbrowser.open("https://youtube.com/")
          self.text_to_speech("Opening YouTube, enjoy your time")
          return "Opening YouTube, enjoy your time"

        elif "open Google" in self.user_input:
          webbrowser.open("https://google.com")
          self.text_to_speech("Opening Google")
          return "Opening Google"

        elif "weather" in self.user_input:
          ans = self.weather()
          self.text_to_speech(ans)
          return ans

        elif "I am not feeling well" in self.user_input:
          webbrowser.open("https://open.spotify.com/")
          self.text_to_speech("Listen to some songs to freshen up your mood")
          return "Listen to some songs to freshen up your mood"

        elif "I am depressed" in self.user_input:
          webbrowser.open("https://youtu.be/eAK14VoY7C0?si=WK1ULquYH__yrqrd")
          self.text_to_speech("Watch this video by Sandeep Maheshwari to overcome depression")
          return "Watch this video by Sandeep Maheshwari to overcome depression"
        
        elif 'Input was not received' in self.user_input:
          self.text_to_speech('Input was not received')
          return 'Input was not received'

        elif "wiki" in self.user_input:
          query = self.user_input.replace("wiki", "").strip()
          try:
            result = wikipedia.summary(query, sentences=2)
            self.text_to_speech(result)
            return result
          except wikipedia.DisambiguationError as e:
            result = f"Ambiguous term. Please specify: {', '.join(e.options)}"
          except wikipedia.PageError:
            result = "No Wikipedia page found for the query."
          self.text_to_speech(result)
          return result
        
        else:
            self.text_to_speech("I am not able to understand")
            return "I am not able to understand"
        

    def search_api(self, query):
     url = "https://chatgpt-api8.p.rapidapi.com/"
     payload = {"query":query} 
     headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "d19ccafbf7mshb20cf6f021509cfp1dc5d8jsn37542c4371bf",
	    "X-RapidAPI-Host": "chatgpt-api8.p.rapidapi.com"
    }

     response = requests.post(url, json=payload, headers=headers)
     return response.json()['response']
    
    def weather(self):
      s = HTMLSession()
      query = "pune"
      url =f"https://www.google.com/search?q=weather+in+{query}"
      r=s.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"})
      temp = r.html.find("span#wob_tm" , first= True).text
      unit = r.html.find("div.vk_bk.wob-unit span.wob_t" , first= True).text
      desc= r.html.find("span#wob_dc" , first= True).text
      return temp+" " + unit+" " + desc

    def text_to_speech(self, text):
        engine = pyttsx3.init()
        time.sleep(0.2)
        engine.say(text)
        engine.runAndWait()
