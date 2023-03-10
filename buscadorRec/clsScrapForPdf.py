from bs4 import BeautifulSoup
import urllib.request
import sys

class Scraping():
	def __init__(self):
		self.url = "http://bo.unsa.edu.ar/"
		self.listaArchivos = []
		self.listaCarpetas = []


	def cargarHTML(self):
		response = urllib.request.urlopen(self.url)
		self.html = BeautifulSoup(response, 'html.parser')



	def cargarCarpetas(self):
		tags = self.html('a')
		for tag in tags:
			carpeta = tag.get('href')
			if(carpeta != 'http://www.unsa.edu.ar/' and carpeta != 'http://validator.w3.org/check/refer' and carpeta != 'http://www.google.com/'):
				urlCarpeta = self.url + carpeta
				self.listaCarpetas.append(urlCarpeta)



	def cargaURLs(self):
		x = 0
		while x < len(self.listaCarpetas):
			carpeta = self.listaCarpetas[x]
			try:
				response = urllib.request.urlopen(carpeta)
				urls = BeautifulSoup(response,'html.parser')
			except:
				print("ERROR 404. No se pudo cargar la página: "+ carpeta)
			else:
				tags = urls('a')
				for tag in tags:
					subdir = tag.get('href')
					if (".pdf" or ".doc" or ".docx" or ".txt" or ".html" or ".htm" or ".xml") in subdir:
						url = carpeta + subdir
						self.listaArchivos.append(url)
			x+=1

	def getListaArchivos(self):
		return self.listaArchivos
def main():
	scraping = Scraping()
	scraping.cargarHTML()
	scraping.cargarCarpetas()
	scraping.cargaURLs()

	listaArchivos = scraping.getListaArchivos()
	print(len(listaArchivos))
	f = open("links.txt",'a')
	for archivo in listaArchivos:
		f.write('\n'+archivo)

	f.close()

if __name__ == '__main__':
	main()