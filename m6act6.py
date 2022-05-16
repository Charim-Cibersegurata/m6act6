#Importem els moduls
import ftplib
import subprocess
import os
import psutil
#Constants per la conexió ftp
HOST 	= "192.168.0.19"
USUARI 	= "carim"
PASSW 	= "carim"
ESTAT 	= "inactiu"
backup	= ""
apacheroot = "/var/www/html/"
#Demanem el directori del servidor ftp on farem la copia
backup 	= input("On es farà la copia?")
#Comprova si el servei web està actiu i aturar-ho
for proc in psutil.process_iter():
	if "apache2" in proc.name().lower():
		os.system("systemctl stop apache2")

#Crear conexió ftp
try:
	ftp = ftplib.FTP(HOST,USUARI,PASSW)
	ftp_directoris = ftp.nlst()
	if backup in ftp_directoris:
		ftp.cwd(backup)
		#else:
			#ftp.mkd(backup)
except:
	print("Error intentant conectar amb ftp")
	exit()

#Recorrer els fitxers i directoris de /var/www/html i guardar-los
fitxers = []
for root,dir,dirfiles in os.walk(apacheroot):
	for file in dirfiles:
		path_file = os.path.join(root, file)
		fitxers.append(path_file)

#Recorrer i enviar els archius
for file in fitxers:
	nombase = file.replace(apacheroot, '')
	try:
		with open(file, 'rb') as txt_file:
			ftp.storlines('STOR {nombase}',txt_file)
	except:
		print("Error intentant pujar",file)

#Iniciem apache
os.system("systemctl start apache2")

#tancar la conexió ftp
ftp.quit()
