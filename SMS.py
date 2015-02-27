import smtplib

class SMS():

   def __init__(self, server = None, from_address = None, password = None):
      self.smtp_server_port = server
      self.smtp_from_address = from_address
      self.smtp_password = password

   def configure(self, server, from_address, password):
      self.smtp_server_port = server
      self.smtp_from_address = from_address
      self.smtp_password = password

   def send_sms(self, from_name, to_addrs, sms_body):
      server = smtplib.SMTP(self.smtp_server_port)
      server.starttls()
      server.login(self.smtp_from_address, self.smtp_password)
      headers = "From: " + from_name + "\n"
      server.sendmail(self.smtp_from_address, to_addrs, headers + sms_body)
      server.quit()

   def generate_message(self, name, table, date):
      message = name.split(" ")[1] + ", your table for " + date.strftime('%m/%d/%Y') + " is Table " + str(table) + "."
      return message
