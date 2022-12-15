
import unittest 
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from google_news import Google, DataBase

class TestGoogle(unittest.TestCase):

    @patch('google_news.requests')
    def test_connection(self, mock_request):

        #mock the request and return ok status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request = mock_response.status_code
        self.assertEqual(mock_request, 200)

    @patch('google_news.Google.find_news_sources')
    def test_find_news_sources(self, mock_sources):

        #create a mock html page
        text = '''<html><body>
                  <span class="vr1PYe">The New York Times</span>
                  <span class="vr1PYe">11Alive</span>
                  <span class="vr1PYe">The Connecticut Mirror</span>
                  <span class="vr1PYe">CNN</span>
                  <span class="vr1PYe">CNN</span>
                  <span class="vr1PYe">Reuters</span>
                  <span class="vr1PYe">CBS News</span>
                  <span class="vr1PYe">BBC News</span>
                  <span class="vr1PYe">The Associated Press</span>
                  <span class="vr1PYe">Axios</span>
                  </body></html>'''

        #assert that we have 10 classes with sample news sources
        soup = BeautifulSoup(text, features='lxml')
        mock_sources = soup.findAll(attrs={'class' : 'vr1PYe'})
        self.assertEqual(len(mock_sources), 10)

class TestDataBase(unittest.TestCase):

    def setUp(self):
        self.mydb = Mock()
        self.cursor = Mock()
        
    @patch('google_news.mysql.connector.connect')
    def test_create_table(self, mock_connect):

        #set up mock cursor
        mock_connect.return_value.cursor.return_value = self.cursor 

        #create instance of DataBase class and call create_table()
        self.mydb = DataBase()
        self.mydb.create_table()

        #assert that cursor executed the expected SQL query
        self.cursor.execute.assert_called_with('''CREATE TABLE newssources (id INT AUTO_INCREMENT PRIMARY KEY,
                                               news_source VARCHAR(50),
                                               times_used INT(10))''')
        
        #assert that the database connection commited the changes
        mock_connect.return_value.commit.assert_called()

    @patch('google_news.DataBase.search_data')
    def test_search_data(self, mock_source):

        #set up mock data acting a function argument 
        mock_source = {
            'CBS News' : 10,
        }

        #set up cursor to return mock values of a news source already present in our db
        #this checks out that values from the 'else' statement from search_data method are correct
        #before we passed them to the update_data method
        #values from 'if' go into write_data() method without change
        self.cursor.fetchall.return_value = [(4,)]
        update_number = self.cursor.fetchall.return_value[0][0] + mock_source['CBS News']
        self.assertEqual(update_number, 14)

    @patch('google_news.DataBase.write_data')
    def test_write_data(self, mock_data):

        #set up mock data 
        mock_data = [('CBS News', 10)]

        #mock insertion of mocked data into db    
        sql = f'INSERT INTO newssources (news_source, times_used) VALUES (%s, %s)'
        values = ('CBS News', 10)
        self.cursor.execute(sql)

        #test the mocked data values
        self.assertEqual(values[1], 10)
        self.assertTrue('CBS' in values[0])

    @patch('google_news.DataBase.update_data')
    def test_update_data(self, mock_update):

        #set up mock data
        mock_update = ['ABC News', 7]

        #mock insertion of mocked data into db
        sql = 'UPDATE newssources SET times_used = %s WHERE news_source = %s'
        values = ('ABC News', 7)
        self.cursor.execute(sql)

        #test the mocked data values
        self.assertEqual(values[1], 7)
        self.assertTrue('ABC' in values[0])

if __name__ == '__main__':
    unittest.main()

        




