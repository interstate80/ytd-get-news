#
#
#
import re, csv, math
from collections import defaultdict
# import pandas as pd

class phrasean:
    
    def __init__(self, tlist): # tlist - list of titles
        # self.ignorechars = {ord(','): '', ord('.'): '', ord(':'): '', ord('!'): '', ord('-'): '', ord('?'): '', ord('/'): '', ord('«'): '', ord('»'): '', ord('–'): '', ord('+'): '', ord('('): '', ord(')'): '', ord('—'): ''}
        self.dict = []
        self.phdict = {}
        self.alphabet = re.compile('[а-яА-Я0-9-]+|[.,:;?!]+')
        try:
            self.tokens = self.gen_tokens(tlist)
            self.trigrams = self.gen_trigrams(self.tokens)
        except Exception as e:
            print('%s' %e)
        
    def gen_tokens(self, lines):
        for line in lines:
            for token in self.alphabet.findall(line):
                yield token
                
    def gen_trigrams(self, tokens):
        t0, t1 = '$', '$'
        for t2 in tokens:
            yield t0, t1, t2
            if t2 in '.!?':
                yield t1, t2, '$'
                yield t2, '$', '$'
                t0, t1 = '$', '$'
            else:
                t0, t1 = t1, t2
    
if __name__ == '__main__':
    print('No standalone run...')