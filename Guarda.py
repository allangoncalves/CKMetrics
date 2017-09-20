#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hmac, os, json, sys

class Guarda():

	def __init__(self):
		self.files = {}
		self.early = {}

	def loadData(self):
		for directory, folderName, file in os.walk("."):
				for name in file:
					if name != ".table":
						fullName = os.path.join(directory, name).decode('unicode-escape')
						self.files[fullName] = None
		
		if os.path.isfile(".table"):
			with open(".table", "r") as input:
				file_str  = input.read()
				self.early = json.loads(file_str)

		self.calculateHash()

		diff = set(self.files.items()) ^ set(self.early.items())
		for d in diff:
			print("{} foi removido".format(d))
#####
	def saveData(self):
		with open(".table", "w") as inputFile:
			jsondata = json.dumps(g.files, ensure_ascii=True, indent=4)
			inputFile.write(jsondata)

	def calculateHash(self):
			for fullName in self.files:
				print("Opening file:{}".format(fullName))
				with open(fullName, "r") as input:
					file_str  = input.read()
					myhash = hmac.new(file_str).hexdigest()
					if fullName not in self.early:
						self.files[fullName] = myhash
						self.early[fullName] = myhash
						print("{} foi adicionado".format(fullName))
					elif not myhash.compare_digest(self.early[fullName]):
						print("{} foi alterado".format(fullName))
						print(myhash)
						ans = raw_input("Deseja salvar as alterações?(S/N)")
						if(ans.lower() == "s"):
							self.files[fullName] = myhash
							self.early[fullName] = myhash
						else:
							self.files[fullName] = self.early[fullName]
					else:
						self.files[fullName] = myhash
						self.early[fullName] = myhash

if __name__ == '__main__':

	if len(sys.argv) >= 2:
		os.chdir(sys.argv[1])
		g = Guarda()
		g.loadData()
		g.saveData()
	else:
		print("Insira o diretório a ser guardado")
