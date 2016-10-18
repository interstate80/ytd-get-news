#
#	парсим mediametrics
#
class MMpageParser:
	def __init__(self, rfile, wrfile):
		src = [rfile, wrfile]
		
	def ReadFromFile(self):
		f = open(src[0], 'r')
		fcont = f.read()
		f.close()
		return str(fcont)
	
	def WriteToFile(self):
		f = open(src[1], 'w')
		#
		f.close()
	
	def parseFeed(self):
		from cssselect import GenericTranslator, SelectorError
		from lxml.etree import fromstring
		
		# xmlstr = self.ReadFromFile()
		# doc = LH.document_fromstring(xmlstr)
		# подготовка расширения для выборки
		try:
			expression = GenericTranslator().css_to_xpath('div.result')
		except SelectorError as SE:
			print('Invalid selector %s.' %SE)
		print(expression)
		try:
			document = fromstring('''<div class="result result-sm clearFix" id="row-153264742" aid="153264742" style="height: 18px; width: 690px; top: 0px; position: absolute; z-index: 1; opacity: 1;">
							  <div class="result-pos" id="result-pos153264742"></div>
							  <div class="result-logo"><a href="?search=russian.rt.com" title="russian.rt.com"><img src="/favicon/russian.rt.com.ico" width="16" height="16" border="0" /></a></div>
							  <div class="result-num" id="visitors_153264742" style="background: #FBB" title="подробнее" onclick="showArticle(153264742)">257</div>
							  <div class="result-link"><a target="_blank" href="http://russian.rt.com/inotv/2016-08-10/Times-Kachestvo-rossijskoj-armii-napugalo" id="id-153264742" onclick="cl('pos-1', this)" title="russian.rt.com">Times: Качество российской армии напугало британских военных</a></div>
							  </div>''')
		except:
			print('Жопня')
			
		[e.get('aid') for e in document.xpath(expression)]
		