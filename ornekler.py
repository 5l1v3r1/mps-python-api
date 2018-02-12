#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  run.py
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
from mps import API

if __name__ == '__main__':
	mps = API()
	
	paket="kernel"

	
	print("#Paket Veritabanı Güncelleme")

	for hatalar in mps.paketVTGuncelle():
		sunucu=hatalar[0]
		hata=hatalar[1]
		if hata:
			print("{} sunucusuna bağlanırken hata oluştu: \n{}".format(sunucu,hata))
		else:
			print("Paket veritabanı {} sunucusundan başarıyla güncellendi.".format(sunucu))


	print("# Kurulu kontrol")

	if mps.kuruluKontrol(paket):
		print("{} sisteminizde kurulu".format(paket))
	else:
		print("{} sisteminizde kurulu değil".format(paket))

	
	
	print("#Kurulack Bağımlılıklar")
	
	for i in mps.bagimliPaketListele(paket):
		liste=i
	print(liste)



	print("#Paket Dosyası İndirme")
	
	for cikti in mps.paketIndir(paket):
		if type(cikti) == float:
			print("{} %{:3.2f} indiriliyor.".format(paket,cikti))
		else:
			print("{} indirilirken hata oluştu: \n{}".format(paket,cikti))

