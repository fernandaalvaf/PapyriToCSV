# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
import lxml
import pandas as pd

os.chdir('..')  # sets the root directory of the project

targets =['730','681']

def unpack(s):
    return "\n".join(map(str, s))


newline = "\n"


class Text:
    """Stores the information about the texts"""

    def __init__(self, tmid):
        self.id = tmid
        self.publications = []
        self.papyriinfo_URL = ''
        self.hgv_data = {'Translations': [],
                         'Date': '',
                         'Subjects': ''}
        self.apis_data = {'Title': '',
                          'Summary': '',
                          'Origin': ''}
        self.ddbdp_data = {'Text': '',
                           'Translation': ''}

    def tm_id(self):
        return self.id

    def get(self):
        info = [self.id, self.papyriinfo_URL, self.hgv_data['Translations'], self.hgv_data['Date'],
                self.hgv_data['Subjects'], self.apis_data['Title'], self.apis_data['Summary'], self.apis_data['Origin'],
                self.ddbdp_data['Text']]

        return info

    def showinfo(self):
        print(f'TM id: {self.id}\n#\tPapyriinfo: {self.papyriinfo_URL}'
              f'\n#\tPublications: \n{unpack(self.publications)}'
              f'\n#\tHGV Data: \n{newline.join(f"{key}: {value}" for key, value in self.hgv_data.items())}'
              f'\n#\tAPIS Data: \n{newline.join(f"{key}: {value}" for key, value in self.apis_data.items())}'
              f'\n#\tDDbDP Data: \n{newline.join(f"{key}: {value}" for key, value in self.ddbdp_data.items())}')

    def outputinfo(self):
        content = (f'#  Publications: \n{unpack(self.publications)}\n'
                   f'\n#  HGV Data: \n'
                   f'Translations: \n{unpack(self.hgv_data["Translations"])}\n'
                   f'Date: {self.hgv_data["Date"]}\n'
                   f'Subjects: {self.hgv_data["Subjects"]}\n'
                   f'\n#  APIS Data: \n'
                   f'Summary: \n {self.apis_data["Summary"]}\n')
        return content

    def get_tmdata(self):
        tmid = str(self.tm_id())
        exec(open('papyritocsv/tmdata.py').read())

    def get_ddbdpdata(self):
        papinfo = self.papyriinfo_URL
        exec(open('papyritocsv/ddbdpdata.py').read())

    def addtmdata(self, publications, papyriinfo_URL):
        self.publications = publications
        self.papyriinfo_URL = papyriinfo_URL

    def addhgvdata(self, translations, date, subjects):
        self.hgv_data['Translations'] = translations
        self.hgv_data['Date'] = date
        self.hgv_data['Subjects'] = subjects

    def addapisdata(self, summary, title, origin):
        self.apis_data['Title'] = title
        self.apis_data['Summary'] = summary
        self.apis_data['Origin'] = origin

    def addpapsdata(self, text, translation):
        self.ddbdp_data['Text'] = text
        self.ddbdp_data['Translation'] = translation



texts_list = []


df = pd.DataFrame(columns=['TMid',
                  'Papyri_info',
                  'HGV_Translations',
                   'HGV_Date',
                   'HGV_Subjects',
                   'APIS_Title',
                   'APIS_Summary',
                   'APIS_Origin',
                   'DDBDP_Text'])
count = 0


for target in targets:
    count += 1
    print(f'Progress: {count / len(targets) * 100}%\nTM {target}')
    t1 = Text(target)
    t1.get_tmdata()
    t1.get_ddbdpdata()
    texts_list.append(t1)

    if len(targets) == 1:
        doctitle = t1.apis_data['Title']

tmids = []
dates = []

for t in texts_list:
    tmids.append(t.id)
    dates.append(t.hgv_data['Date'])

for text in texts_list:
    row1 = text.get()
    df.loc[len(df.index)] = row1

csvname = input('Name your csv:')


df.to_csv(f'Saved CSVs/{csvname}.csv', index=False)