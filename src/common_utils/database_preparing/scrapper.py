from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import re
from csvWriter import CsvWriter
from configuration import Configuration
from shortcutsExpander import ShortcutsExpander

class Scrapper:
    def __init__(self):
        self.ITERS_NUM = Configuration.ITERS_NUM.value
        self.DATE = Configuration.DATE.value
        self.STARTING_URL = Configuration.STARTING_URL.value
        # suggested format: 'urls_<yymmdd>_<number_of_iterations>
        self.URLS_CSV_FILENAME = 'csv_files/urls_' + self.DATE + '_' + str(self.ITERS_NUM) + '.csv'
        self.DB_NAME = 'db_' + self.DATE + '_' + str(self.ITERS_NUM)
        # suggested format: 'db_<yymmdd>_<number_of_iterations>.csv'
        self.DB_CSV_FILENAME = 'csv_files/' + self.DB_NAME + '.csv'
        # {<url>, <URL has already been searched for new links>}
        self.urls_to_search = {self.STARTING_URL: False}
        self.polish_words_map = {}
        self.CHROME_WEB_DRIVER = webdriver.Chrome(executable_path=Configuration.CHROME_DRIVER_PATH.value)
        self.DB_CSV_WRITER = CsvWriter(self.DB_CSV_FILENAME)

    def main(self):
        i = 0
        while i < self.ITERS_NUM:
            print(i)
            url_to_search_through = self.get_next_url_to_search_through()
            if url_to_search_through is None:
                break
            self.CHROME_WEB_DRIVER.get(url_to_search_through)
            data = self.get_data(self.CHROME_WEB_DRIVER.page_source, url_to_search_through)
            self.save_data(data)
            self.urls_to_search[url_to_search_through] = True  # mark current URL as already searched
            other_relative_urls = self.find_other_relative_urls(self.CHROME_WEB_DRIVER.page_source)
            self.add_new_urls(other_relative_urls)
            i += 1
        self.save_urls_list()

    def get_next_url_to_search_through(self):
        for url, wasSearched in self.urls_to_search.items():
            if wasSearched == False:
                return url
        return None

    def get_data(self, content, url):
        tags = self.get_tags(url)
        soup = BeautifulSoup(content, features="html.parser")
        whole_page_text = ""
        for bodytext in soup.findAll("p", "bodytext"):
            text = str(bodytext)
            if len(text) > 50:
                first_letter = text.find('>') + 1
                text = text[first_letter:]
                last_letter = text.find('<')
                text = text[:last_letter]
                while len(text) > 0 and text[len(text) - 1] == '\n':
                    text = text[:-1]
                if len(text) > 0:   # could be 0, for example:<p class="bodytext"><a class="external-link-new-window" href=...>
                    whole_page_text += (' ' + text)
        return [tags, whole_page_text]

    def get_tags(self, url):
        url = url[len(self.STARTING_URL):]
        tags = url.split('/')
        for i in range(len(tags)):
            tags[i] = tags[i].split('-')
        tags_list = list(itertools.chain.from_iterable(tags))
        for i in range(len(tags_list)):
            tags_list[i] = tags_list[i].lower()
            if tags_list[i] in self.polish_words_map:
                tags_list[i] = self.polish_words_map[tags_list[i]]
        tags_list.remove('')
        return tags_list

    def save_data(self, data):
        tags = data[0]
        whole_page_text = data[1]
        if len(whole_page_text) > 20:
            self.DB_CSV_WRITER.write_tags_and_text(tags, whole_page_text)

    def find_other_relative_urls(self, content):
        soup = BeautifulSoup(content, features="html.parser")
        relative_urls=[]
        for link in soup.find_all('a'):
            link_as_str = link.get('href')
            if link_as_str is None or link_as_str == '/':
                continue
            if self.is_relative(link_as_str):
                relative_urls.append(link_as_str)
                whole_link_str = str(link)
                words = re.split('\"|<|>|=|/|-| ', whole_link_str)
                for word in words:
                    word = word.lower()
                    if self.has_polish_char(word):
                        self.polish_words_map[self.delete_polish_chars(word)] = word
        self.delete_ending_slash(relative_urls)
        return relative_urls

    def is_relative(self, link):
        str_len = len(link)
        if str_len <= 2:
            return False
        return link[0] == '/' and link[str_len - 1] == '/'

    def has_polish_char(self, word):
        for letter in word:
            if letter in'ąćęłóśżź':
                return True
        return False

    def delete_polish_chars(self, word):
        word = word.replace('ą', 'a')
        word = word.replace('ć', 'c')
        word = word.replace('ę', 'e')
        word = word.replace('ł', 'l')
        word = word.replace('ó', 'o')
        word = word.replace('ś', 's')
        word = word.replace('ż', 'z')
        word = word.replace('ź', 'z')
        return word

    def delete_ending_slash(self, relative_urls):
        for i in range(len(relative_urls)):
            relative_urls[i] = relative_urls[i][:-1]

    def add_new_urls(self, other_urls):
        for relative_url in other_urls:
            url = self.STARTING_URL + relative_url
            if url not in self.urls_to_search:
                self.urls_to_search[url] = False

    def save_urls_list(self):
        urls_list = []
        for k, v, in self.urls_to_search.items():
            urls_list.append(k)
        df = pd.DataFrame({'url address': urls_list})
        df.to_csv(self.URLS_CSV_FILENAME, index=False, encoding='utf-8')

def main():
    scrapper = Scrapper()
    scrapper.main()
    SHORTCUT_DB_CSV_FILENAME = 'csv_files/' + scrapper.DB_NAME + '_shortcutsExpanded.csv'
    ShortcutsExpander().expand_shortcuts(scrapper.DB_CSV_FILENAME, SHORTCUT_DB_CSV_FILENAME)

main()