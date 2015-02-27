from PDFReader import PDFReader
from SMS import SMS
import datetime
import os.path
from time import sleep
import json
import urllib2

def load_smtp_configuration():
    json_config = open('config/smtp_configuration.json')
    config = json.load(json_config)

    smtp_server = str(config["smtpServer"])
    smtp_from_address = str(config["smtpFromAddress"])
    smtp_password = str(config["smtpFromAddressPassword"]) 

    return smtp_server, smtp_from_address, smtp_password

def load_users():
   users_file = open('config/users.json')
   users_json = json.load(users_file)

   return users_json

def load_dates():
   dates = []
   dates.append(datetime.date(2015,1,7))
   dates.append(datetime.date(2015,1,9))
   dates.append(datetime.date(2015,1,12))
   dates.append(datetime.date(2015,1,14))
   dates.append(datetime.date(2015,1,21))
   dates.append(datetime.date(2015,1,23))
   dates.append(datetime.date(2015,1,26))
   dates.append(datetime.date(2015,1,28))
   dates.append(datetime.date(2015,1,30))
   dates.append(datetime.date(2015,2,2))
   dates.append(datetime.date(2015,2,4))
   dates.append(datetime.date(2015,2,6))
   dates.append(datetime.date(2015,2,9))
   dates.append(datetime.date(2015,2,11))
   dates.append(datetime.date(2015,2,13))
   dates.append(datetime.date(2015,2,16))
   dates.append(datetime.date(2015,2,18))
   dates.append(datetime.date(2015,2,20))
   dates.append(datetime.date(2015,2,23))
   dates.append(datetime.date(2015,2,25))
   dates.append(datetime.date(2015,2,27))
   dates.append(datetime.date(2015,3,9))
   dates.append(datetime.date(2015,3,11))
   dates.append(datetime.date(2015,3,13))
   dates.append(datetime.date(2015,3,16))
   dates.append(datetime.date(2015,3,18))
   dates.append(datetime.date(2015,3,20))
   dates.append(datetime.date(2015,3,23))
   dates.append(datetime.date(2015,3,25))
   dates.append(datetime.date(2015,3,27))
   dates.append(datetime.date(2015,3,30))
   dates.append(datetime.date(2015,4,1))
   dates.append(datetime.date(2015,4,3))
   dates.append(datetime.date(2015,4,6))
   dates.append(datetime.date(2015,4,8))
   dates.append(datetime.date(2015,4,10))
   dates.append(datetime.date(2015,4,13))
   dates.append(datetime.date(2015,4,15))
   dates.append(datetime.date(2015,4,17))
   dates.append(datetime.date(2015,4,20))
   dates.append(datetime.date(2015,4,22))

   return dates

def run():

   url_to_seating_charts = "http://cise.ufl.edu/~jnw/CAP6137/Seating/"

   names_of_interest = ["Bruch Austin F", "Jacobsen Connor A", "Bujduveanu Alexander T"]

   # Create a list of days that we have class
   # The index in the list corresponds to the class "number" (off by one because of 0-index)
   
   load_smtp_configuration()

   dates = load_dates()

   _dict = load_users()

   class_number = 0

   today = datetime.date.today()
   for i in range(0, len(dates)): # Determine which class number today is by comparing each date in the list to today's date
      if dates[i] == today:
         class_number = i+1

   if class_number == 0:
      # Today's date didn't match any class date in the list
      print "There's no class today."
      return

   url_to_seating_chart = url_to_seating_charts + "Class" + str(class_number) + ".pdf"

   # Dictionary containing names according to the seating charts, and SMS Gateway email addresses to send an SMS
   _dict = {
            "Bruch Austin F": "7272549322@vtext.com"
         }

   sms_sender = SMS() # Utility that generates SMS messages and sends them
   pdf_reader = PDFReader() # Utility that parses PDF documents

   server, from_addr, password = load_smtp_configuration()
   sms_sender.configure(server, from_addr, password)

   try:
      text = pdf_reader.read_pdf_from_url(url_to_seating_chart)
   except urllib2.HTTPError as e:
      if e.code == 404:
         print "Today's Seating Chart has not been posted."
      return

   # If we get this far, the file has been read successfully from the course website
   lines = text.split('\n')
   for line in lines:
      linesplit = line.split(':') # Student name comes before a colon, the table number comes after it
      if len(linesplit) > 1: # As long as we're on a line that had a colon in it
         name = linesplit[0].strip()
         for _name in names_of_interest:
            if _name == name: # the name from the file matches a name of interest
               temp = linesplit[1].strip()
               table = temp[0]
               
               if name in _dict: # As long as we have an sms address for the name of interest
                  print "Sending sms to: " + name
                  sms_body = sms_sender.generate_message(name, table, dates[class_number-1])
                  sms_sender.send_sms("Malware Seating Assignment", _dict[name], sms_body) # uncomment this line to actually send the SMS


def main():

   # run()
   # return
   while(True):
      current_time = datetime.datetime.now().time()
      if current_time.hour == 12 and current_time.minute == 40: # send the SMS messages at 12:40pm (10 minutes before class starts)
         # run the code to send the text
         run()
         sleep(60) # Sleep for a minute so we know that when the loop comes back around, it wont send another SMS
      else:
         if current_time.hour <= 10:
            print "[" + str(current_time) + "] sleeping for an hour"
            sleep(60*60)
         elif current_time.hour > 12:
            print "[" + str(current_time) + "]sleeping for 6 hours"
            sleep(60*60*6)
         else:
            print "[" + str(current_time) + "]sleeping for " + str(60 - current_time.second) + " seconds"
            sleep(60 - current_time.second)

if __name__ == '__main__':
   main()


