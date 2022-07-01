
import requests, mysql.connector
from bs4 import BeautifulSoup

class Google:

    def __init__(self):
        self.url = 'https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en'
        self.news = requests.get(self.url)
        self.soup = BeautifulSoup(self.news.text, 'html.parser')

    def find_news_sources(self) -> list:
        self.titles = self.soup.select(selector = '.wEwyrc.AVN2gc.uQIVzc.Sksgp')
        return self.titles

class DataBase:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'password',
            database = 'GoogleNews'
            )

        self.cursor = self.mydb.cursor()

    def create_table(self):

        self.sql = '''CREATE TABLE newssources (id INT AUTO_INCREMENT PRIMARY KEY,
                                               news_source VARCHAR(50),
                                               times_used INT(10))'''

        self.cursor.execute(self.sql)
        self.mydb.commit()

    def search_data(self, s_news) -> None:
        
        for key, value in s_news.items():
            self.sql = f'SELECT times_used FROM newssources WHERE news_source = "{key}"'
            self.cursor.execute(self.sql)
            self.number = self.cursor.fetchall()
            
            if self.number == []:
                self.write_data(key, value)
            else:
                update_search_numbers = self.number[0][0] + value
                self.update_data(key, update_search_numbers)

    def write_data(self, w_name, w_number) -> None:

        self.sql = 'INSERT INTO newssources (news_source, times_used) VALUES (%s, %s)'
        self.val = (w_name, w_number)

        self.cursor.execute(self.sql, self.val)
        self.mydb.commit()

    def update_data(self, u_name, u_data) -> None:
        
        self.sql = 'UPDATE newssources SET times_used = %s WHERE news_source = %s'
        self.val = (u_data, u_name)
        self.cursor.execute(self.sql, self.val)
        self.mydb.commit()

def main():
    google = Google()
    sources = google.find_news_sources()
    news_outlet = {}

    for name in sources:
        if name.text in news_outlet:
            news_outlet[name.text] += 1
        else:
            news_outlet.setdefault(name.text, 1)

    db = DataBase()
    db.search_data(news_outlet)

if __name__ == '__main__':
    main()
