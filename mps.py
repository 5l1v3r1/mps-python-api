#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mps.py
#  
#  Copyright 2018 geekdinazor <furkan.kalkan3@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os,urllib.error
import urllib.request
class API :
	""" Milis Paket Sistemi işlemleri için native Python kütüphaneleri """
	
	def __init__ (self):
		self.paketDizin="/var/lib/pkg/DB"
		self.ayarDosya="/etc/mps.conf"
		self.ayarlar={}
		self.__ayarDosyaOku()
		#self.paketDepo="/depo/paketler/"
		self.paketDepo=""
		self.talimatDepo="/root/talimatname"

	def __ayarDosyaOku(self):
		f=open(self.ayarDosya,'r')
		satirlar=f.readlines()
		if satirlar[0][0]!='#':
			self.ayarlar["sunucu"] = satirlar[0].split('"')[1::2][0]
		if satirlar[1][0]!='#':
			self.ayarlar["sunucular"] = satirlar[1].split('"')[1::2][0].split(' ')
		if satirlar[2][0]!='#':
			self.ayarlar["lokal"] = satirlar[1].split('"')[1::2][0]
		if satirlar[3][0]!='#':
			self.ayarlar["docsil"] = satirlar[1].split('"')[1::2][0]
		if satirlar[4][0]!='#':
			self.ayarlar["yerelsil"] = satirlar[1].split('"')[1::2][0]
		if satirlar[5][0]!='#':
			self.ayarlar["ektalimatname"] = satirlar[1].split('"')[1::2][0]

	def dosyaIndir(self,url,dosya,sessiz):
		f=open(dosya, 'wb')
		parca_boyut=16*1024
		if sessiz:
			try:
				u=urllib.request.urlopen(url)
				while True:
					parca = u.read(parca_boyut)
					if not parca:
						break
					f.write(parca)
				yield None
			except urllib.error.HTTPError as e:
				yield e
				os.remove(dosya)
		else:
			try:
				u=urllib.request.urlopen(url)
				i=0
				toplam_boyut=u.length
				while True:
					i+=1
					parca = u.read(parca_boyut)
					if not parca:
						break
					yield ((i*parca_boyut)/toplam_boyut)*100
					f.write(parca)
			except urllib.error.HTTPError as e:
				print(e)
				os.remove(dosya)
	
	def paketVTGuncelle(self):
		i=0
		for sunucu in self.ayarlar["sunucular"]:
			i+=1
			if i > 1:
				paketvt="{}paket{}.vt".format(self.paketDepo,i)
			else:
				paketvt="{}paket.vt".format(self.paketDepo)	
			url="http://{}{}".format(sunucu,paketvt)
			for hatalar in self.dosyaIndir(url,paketvt,sessiz=True):
				yield [sunucu,hatalar]

	def paketIndir(self,paket):
		i=0
		dosya=None
		for sunucu in self.ayarlar["sunucular"]:
			i+=1
			if i > 1:
				paketvt="{}paket{}.vt".format(self.paketDepo,i)
			else:
				paketvt="{}paket.vt".format(self.paketDepo)	
				
				f=open(paketvt,'r')
				f=f.read().replace("\n"," ").split(" ")
				try:
					dosya=f[f.index(paket)+2]	
					url="http://{}{}".format(sunucu,dosya.replace("#","%23"))
				except ValueError as e:
					yield "İstenilen paket veritabanında bulunamadı."
		if dosya:
			for cikti in self.dosyaIndir(url,dosya,sessiz=False):
				yield cikti
	
	def kuruluKontrol(self, paket):
		if paket in os.listdir(self.paketDizin):
			return True
		else:
			return False	

	def kurulacakBagimliliklar(self,paket,**kwargs):
		if not "name" in kwargs.keys():
			tumbag=set()
		else:
			tumbag=kwargs["tumbag"]
		for dizin, altdizin, dosya in os.walk(self.talimatDepo):
			if dizin.split("/")[-1] == paket:
				talimat=open("{}/talimat".format(dizin),"r")
				satir=talimat.read().splitlines()[3]
				if "# Gerekler:" in satir:
						satir = satir.split(':')[1]
						bagimliliklar = satir.split(" ")
						for bagimlilik in bagimliliklar:
							if len(bagimlilik) > 0:
								if not bagimlilik in tumbag: 
									if not self.kuruluKontrol(bagimlilik):
										tumbag.add(bagimlilik)
										for i in self.kurulacakBagimliliklar(bagimlilik,tumbag=tumbag):
											for bagimlilik in i:
												tumbag.add(bagimlilik)
										tumbag.add(paket)
										yield(list(tumbag))
