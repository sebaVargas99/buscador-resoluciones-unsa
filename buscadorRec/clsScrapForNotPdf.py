#Probando beautifulsoup
from bs4 import BeautifulSoup
import urllib.request


class Scrap():
	def __init__(self):
		self.__url = "http://bo.unsa.edu.ar/"

	def ingresarCarpeta(self, carpeta, lista):
		if "http" not in carpeta and carpeta not in lista:
			lista.append(carpeta)

	def ingresarArchivo(self, archivo, lista):
		if("pdf" or "doc" or "docx" or "txt" or ".html" or ".htm" or ".xml") in archivo:
			lista.append(archivo)

	def identificaAnio(self, carpeta):
		anio = str(carpeta)
		anio = anio[1:-1]
		return anio

	def identificaRazon(self, carpeta):
		razon = str(carpeta)
		razon = razon[0]
		return razon

	def identificaTipo(self, archivo):
		tipo = "None"
		if "pdf" in archivo:
			tipo = "PDF"
		elif "html" in archivo:
			tipo = "HTML"
		elif "htm" in archivo:
			tipo = "HTM"
		elif "xml" in archivo:
			tipo = "XML"
		elif "doc" in archivo:
			tipo = "DOC"
		elif "docx" in archivo:
			tipo = "DOCX"
		elif "txt" in archivo:
			tipo = "TXT"
		return tipo

	def scraping(self,url):
		listaCarpetas = []
		listaArchivos = []
		try:
			data = urllib.request.urlopen(url)
			sopa = BeautifulSoup(data, 'html.parser')
		except:
			print( "ERROR 404 - NO se cargo la diirección "+ url)
		else:
			tags = sopa('a')
			listaCarpetas.append("/")
			for tag in tags:
				carpeta = tag.get('href')
				index = carpeta.find("/")
				if(index != -1):
					carpeta = carpeta[:index + 1]
					self.ingresarCarpeta(carpeta,listaCarpetas)
				elif ";" not in carpeta:
					archivo = url + carpeta
					#print("url de archivo: " + archivo)
					listaArchivos.append(archivo)

		return listaCarpetas, listaArchivos


	def cargar(self):
		print("comenzando scraping en "+ self.__url)
		listaOrg,listaArchivos = self.scraping(self.__url)
		listaLink = []
		print("fase 1:")
		print("carpeta ORG:")
		print("lista de archivos")
		for org in range(1,len(listaOrg)):
			listaAnios, listaArchivos = self.scraping(self.__url + listaOrg[org])
			print("fase 3:")
			for j in range(1,len(listaAnios)):
				subcarpeta,listaArchivos = self.scraping(self.__url + listaOrg[org]+listaAnios[j])
				razon = self.identificaRazon(listaAnios[j])
				anio = self.identificaAnio(listaAnios[j])
			if len(listaArchivos) != 0:
				for archivo in listaArchivos:
					tipo = self.identificaTipo(archivo)
			for k in range(1, len(subcarpeta)):
				print("comenzando scraping en "+ self.__url + listaOrg[org] + listaAnios[j] + subcarpeta[k])
				finDeScrap, listaArchivos = self.scraping(self.__url + listaOrg[org] + listaAnios[j] + subcarpeta[k])
				if len(listaArchivos)!=0:
					for archivo in listaArchivos:
						tipo = self.identificaTipo(archivo)
						print("direccion del archivo: "+ archivo)
						listaLink.append(archivo)
		for link in listaLink:
			print(link)
		print("cantidad de archivos : "+ str(len(listaLink)))
		return listaLink,listaAnios,listaOrg

	def getListaAnios(self):
		print("comenznando scraping en "+self.__url)
		listaOrg, listaArchivos

def main():
	scrap = Scrap()
	archivos,anios,organizaciones = scrap.cargar()

	txtArchivos = open("listaLinks.txt","a")
	for archivo in archivos:
		txtArchivos.write("\n"+archivo)
	txtArchivos.close

	txtAnios = open("listaAnios.txt","a")
	for anio in anios:
		txtAnios.write("\n"+anio)
	txtAnios.close

	txtOrg = open("listaOrg.txt","a")
	for org in organizaciones:
		txtOrg.write("\n"+org)
	txtOrg.close
if __name__ == '__main__':
	main()
