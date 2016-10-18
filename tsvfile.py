#
#   Работа с tsv
#
import csv, re

class tsvfile:
    
    def __init__(self, tsvfpath):
        if not tsvfpath:
            print('Не задан файл.')
        else:
            print('Задан файл: %s.' %tsvfpath)
            self.filepaths = tsvfpath
            
    def getrows(self):
        with open(self.filepaths, 'r', encoding='utf-8') as stvs:
            for line in csv.reader(stvs, dialect='excel-tab'):
                print(line[1])
        stvs.close()
    
    def gettitles_to_list(self):
        tlist = []
        with open(self.filepaths, 'r', encoding='utf-8') as stvs:
            for line in csv.reader(stvs, dialect='excel-tab'):
                tlist.append(line[1])
        stvs.close()
        return tlist

if __name__ == '__main__':
    print('Отсутствует механизм самостоятельного выполнения.')
