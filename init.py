#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import zipfile
import os
from string import Template

class Author(dict):
    def __init__(self):
        self['Name'] = ''          # 自分の名前（日本語）
        self['Roman'] = ''         # 自分の名前（ローマ字）
        self['StudentNumber'] = '' # 学生証番号
        self['SuperVisor'] = ''    # 指導教員の名前
        self['Degree'] = ''        # 「博士」，「修士」or「学士」
        self['Affiliation'] = ''   # 所属学部を書く．
        # 以下の変数は自動的に更新される．
        self['Year'] = self.parse_time()
        self['EraYear'] = self['Year'] - 2018
        self['TargetName'] = ''

    def parse_time(self):
        date = datetime.datetime.today()
        year = date.year
        if date.month >= 1 and date.month <= 3:
            year = year - 1
        return year

    def build_targetname(self):
        roman = self['Roman']
        last, first = roman.split(' ')
        last = last.lower()
        file = 'bthesis'
        if self['Degree'] == '修士':
            file = 'mthesis'
        elif self['Degree'] == '博士':
            file = 'dthesis'

        self['TargetName'] = last + str(self['Year'])[:-2] + file

class ThesisInitializer:
    def __init__(self):
        self.parse_author()
        self.create_files()
        self.remove_unused()
        self.keywords = [ 'Degree', 'EraYear', 'TargetName', 'Name', 'StudentNumber', 'SuperVisotr', 'Affiliation' ]

    def create_files(self):
        base = self.author['TargetName']

        with zipfile.ZipFile('init.zip', 'r') as post:
            self.output(post, 'csg-thesis.bst', 'csg-thesis.bst')
            self.output(post, 'csg-thesis.sty', 'csg-thesis.sty')
            self.output(post, 'url.sty', 'url.sty')
            self.output(post, '.gitignore', '.gitignore')
            self.filter_output(post, 'Makefile', 'Makefile')
            self.filter_output(post, 'thesis_format.tex', base + '.tex')
            self.touch(base + '.bib')

            post.close()

    def touch(self, dest):
        out = open(dest, 'w')
        out.write('')
        out.close()

    def filter_output(self, post, source, dest):
        data = post.read(source)
        out = open(dest, 'w')
        t = Template(data)
        data = t.safe_substitute(self.author)
        out.write(data)
        out.close()
        
    def output(self, post, source, dest):
        out = open(dest, 'w')
        out.write(post.read(source))
        out.close()

    def remove_unused(self):
        pass

    def parse_author(self):
        fp = open('author.txt', 'r')
        self.author = Author()

        for line in fp:
            line = line.strip()
            if not line.startswith('#'):
                key, value = line.split(':')
                key = key.strip()
                value = value.strip()
                self.author[key] = value
        self.author.build_targetname()
        print self.author

        fp.close()
                

if __name__ == '__main__':
    ThesisInitializer()
