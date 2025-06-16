from bs4 import BeautifulSoup

class HtmlToText:
  def __init__(self, html_content):
    self.html_content = html_content

  def convert(self):
    soup = BeautifulSoup(self.html_content, 'html.parser')
    return soup.get_text()