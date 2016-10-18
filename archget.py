#!/usr/bin/env python
# -*- coding: utf-8 -*
#

from datetime import datetime
from urllib import request as UReq
import zipfile, os
from tsvfile import tsvfile
from analyze import txtanalyzer
from phraze import phrasean as PA

class mmarch:
	
	params = ['ru','hour']
	baseurl = 'http://mediametrics.ru/data/archive/'
	
	def __init__(self):
		self.arfname = self.filename(True)
		self.efname = self.params[1] + '/' + self.filename(False) + '_23:59:00.tsv' # имя файла в архиве
		self.efnamereal = self.efname.replace(':', '_') # имя распакованного файла (':' заменено на '_')
		furl = self.baseurl + self.params[1] + '/' + self.arfname
		if os.path.exists(self.arfname):
			if os.path.isfile(self.arfname):
				print('Архив %s найден.' %self.arfname)
				if os.path.exists(self.efnamereal): print('Файл %s уже распакован.' %self.efname)
				else: self.extractfile()
		else:
			print('Архив не найден.\nСкачиваем архив %s...' %furl)
			self.getfile(furl)
			self.extractfile()
			# self.delzipfile()
		self.tsvf = tsvfile(self.efnamereal)
		self.docs = self.tsvf.gettitles_to_list()
		
		# if input('Производим анализ по фразам? [y/n]: ') == 'n':
			# self.phrazes = PA(self.docs)
		#elif 
		# else:
		txtanalyzer(self.docs)
		print('Завершаем работу.')
		
		
	def filename(self, isfull):
		# генерирует имя файла для архива и для распаковки
		dt = datetime.today().date()
		dt = dt.replace(day=dt.day-1)
		if isfull: archname = self.params[0] + '-' + dt.isoformat() + '.zip'
		else: archname = self.params[0] + '-' + dt.isoformat()
		return str(archname)
	
	def getfile(self, furl):
		# скачивает файл архива
		fpath = str(self.arfname)
		fr = open(fpath, 'wb')
		try:
			with UReq.urlopen(furl) as ff:
				s = ff.read()
		except Exception as eee:
			print('ОШИБКА!\n %s' %eee)
		fr.write(s)
		fr.close()
	
	def delzipfile(self):
		# if raw_input('Удалить файл с архивом? [y/n]') == 'y'
		path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.arfname)
		print('Удаляем *.zip файл %s' %path)
		os.remove(path)
			
		
	def extractfile(self):
		# распаковывает файл из архива
		try:
			zf = zipfile.ZipFile(self.arfname, 'r')
		except Exception as eee:
			print('Ошибка!')		
		try:
			print('Распаковываем файл %s...' %self.efname)
			zf.extract(self.efname)
			print('Готово.')
		except Exception as eee:
			print('Ошибка распаковки: %s' %eee)
		zf.close()
		
		
if __name__ == '__main__':
	archh = mmarch()
