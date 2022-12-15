
import requests, mysql.connector
from bs4 import BeautifulSoup

class Google:

    def __init__(self) -> None:
        self.url = 'https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en'

    def connect_url(self) -> requests.models.Response:
        response = requests.get(self.url)
        return response
    
    def find_news_sources(self, google_data) -> list:
        soup = BeautifulSoup(google_data.text, 'html.parser')
        news_sources = soup.find_all('span', class_ = 'vr1PYe')
        return news_sources

class DataBase:

    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'password',
            database = 'GoogleNews'
            )

        self.cursor = self.mydb.cursor()

    def create_table(self) -> None:

        sql = '''CREATE TABLE newssources (id INT AUTO_INCREMENT PRIMARY KEY,
                                               news_source VARCHAR(50),
                                               times_used INT(10))'''

        self.cursor.execute(sql)
        self.mydb.commit()

    def search_data(self, s_news: dict[str, int]) -> None:
        
        for key, value in s_news.items():
            sql = f'SELECT times_used FROM newssources WHERE news_source = "{key}"'
            self.cursor.execute(sql)
            number = self.cursor.fetchall()
            
            if number == []:
                self.write_data(key, value)
            else:
                update_search_numbers = number[0][0] + value
                self.update_data(key, update_search_numbers)

    def write_data(self, w_name: str, w_number: int) -> None:

        sql = 'INSERT INTO newssources (news_source, times_used) VALUES (%s, %s)'
        val = (w_name, w_number)

        self.cursor.execute(sql, val)
        self.mydb.commit()

    def update_data(self, u_name: str, u_data: int) ->  None:
        
        sql = 'UPDATE newssources SET times_used = %s WHERE news_source = %s'
        val = (u_data, u_name)
        self.cursor.execute(sql, val)
        self.mydb.commit()

def main():
    google = Google()
    response = google.connect_url()
    sources = google.find_news_sources(response)
    news_outlets = {}

    for name in sources:
        if name.text in news_outlets:
            news_outlets[name.text] += 1
        else:
            news_outlets[name.text] = 1

    db = DataBase()
    db.search_data(news_outlets)

if __name__ == '__main__':
    main()
