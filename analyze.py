#
#   разбор текста
#
# from collections import Counter
# from pyparsing import Word, alphas
import numpy as np
import re, csv, math
from nltk.stem.snowball import SnowballStemmer

class txtanalyzer(object):
    
    def __init__(self, docs):
        self.wdict = {}
        self.dictionary = []
        self.ignorechars = {ord(','): '', ord('.'): '', ord(':'): '', ord('!'): '', ord('-'): '', ord('?'): '', ord('/'): '', ord('«'): '', ord('»'): '', ord('–'): '', ord('+'): '', ord('('): '', ord(')'): '', ord('—'): ''}
        categories = ['общество', 'политика', 'экономика', 'наука', 'культура', 'спорт', 'происшествия']
        # self.stopwords = self.getstopwordslist()
        self.ddocs = []
        self.stemmer = SnowballStemmer('russian', True)
        for doc in docs:
            if type(doc) == list:
                continue
            else:
                self.add_doc(doc)
        # self.print_svd()
        #self.dump_src()
        # fndword = input('Слово для поиска: ')
        for fndword in categories:
            ir = 0
            print('В категории %s.' %fndword)
            for res in self.find(fndword):
                ir += 1
                print(res[0], docs[res[0]])
                if ir == 10: break
    
    def prepare(self):
        self.build()
        self.calc()
        self.TFIDF()
                              
    def dic(self, word, add = False):
        word = word.lower().translate(self.ignorechars)
        word = self.stemmer.stem(word)
        if word.__len__() > 0 and word not in self.stemmer.stopwords:
            if word in self.dictionary:
                return self.dictionary.index(word)
            else:
                if add:
                    self.dictionary.append(word)
                    return len(self.dictionary) - 1
                else:
                    return None
        else:
            return None
    
    def add_doc(self, doc):
        words = [self.dic(word, True) for word in doc.lower().split() if self.dic(word, True)]
        self.ddocs.append(words)
        for word in words:
            if word in self.wdict:
                self.wdict[word].append(len(self.ddocs) - 1)
            else:
                self.wdict[word] = [len(self.ddocs) - 1]

    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        self.A = np.zeros([len(self.keys), len(self.ddocs)])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i, d] += 1
    
    def calc(self):
        self.U, self.S, self.Vt = np.linalg.svd(self.A)
        
    def TFIDF(self):
        wordsPerDoc = np.sum(self.A, axis=0)
        # print(wordsPerDoc)
        docsPerWord = np.sum(np.asarray(self.A > 0, 'i'), axis=1)
        # print(docsPerWord)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                if wordsPerDoc[j] == 0:
                    continue
                else:
                    self.A[i,j] = (self.A[i,j] / wordsPerDoc[j]) * math.log(float(cols) / docsPerWord[i])
    
    def dump_src(self):
        self.prepare()
        for i, row in enumerate(self.A):
            print(self.dictionary[i], row)
        
    def print_svd(self):
        self.prepare()
        # print(self.S)
        for i, row in enumerate(self.U):
            print(self.dictionary[self.keys[i]], row[0:3])
        print(-1*self.Vt[0:3, :])
        
    def find(self, word):
        self.prepare()
        # self.dump_src()
        idx = self.dic(word)
        if not idx:
            print('Слово не встречается.')
            print(idx)
            return []
        if not idx in self.keys:
            # print(self.keys)
            print('В стопвордах')
            return []
        idx = self.keys.index(idx)
        print('word -', word, '=', self.dictionary[self.keys[idx]], '.\n')
        wx, wy = (-1 * self.U[:, 1:3])[idx]
        print('{}\t{:0.2f}\t{:0.2f}\t{}\n'.format(idx, wx, wy, word))
        arts = []
        xx, yy = -1 * self.Vt[1:3, :]
        for k, v in enumerate(self.ddocs):
            ax, ay = xx[k], yy[k]
            dx, dy = float(wx - ax), float(wy - ay)
            arts.append((k, v, ax, ay, math.sqrt(dx * dx + dy * dy)))
        return sorted(arts, key = lambda a: a[4])
    
if __name__ == '__main__':
    print('Отсутствует механизм самостоятельного выполнения.')