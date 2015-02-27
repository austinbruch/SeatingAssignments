from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

from urllib2 import Request
import urllib2

class PDFReader():
   
   def __init__(self):
      # Initialize the PDFReader
      pass

   def read_pdf(self, path_to_pdf):
      resource_manager = PDFResourceManager()
      return_string = StringIO()
      encoding = 'utf-8'
      la_params = LAParams()
      device = TextConverter(resource_manager, return_string, codec=encoding, laparams=la_params)


      interpreter = PDFPageInterpreter(resource_manager, device)

      pdf_file_pointer = file(path_to_pdf, 'rb')

      for page in PDFPage.get_pages(pdf_file_pointer):
         interpreter.process_page(page)

      text = return_string.getvalue()

      pdf_file_pointer.close()
      device.close()
      return_string.close()

      return text

   def read_pdf_from_url(self, url):

      online_pdf = urllib2.urlopen(Request(url)).read()
      file_pointer = StringIO(online_pdf)

      resource_manager = PDFResourceManager()
      return_string = StringIO()
      encoding = 'utf-8'
      la_params = LAParams()
      device = TextConverter(resource_manager, return_string, codec=encoding, laparams=la_params)


      interpreter = PDFPageInterpreter(resource_manager, device)

      for page in PDFPage.get_pages(file_pointer):
         interpreter.process_page(page)

      text = return_string.getvalue()

      file_pointer.close()
      device.close()
      return_string.close()

      return text
