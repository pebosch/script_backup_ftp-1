import ftplib
import os
import shutil
import ftplib
import logging
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.DEBUG)

# Guardamos el directorio en una variable
directorio = "/home/enrique/public_html"

# Creamos la copia comprimida y la guaradamos en una variable
shutil.make_archive("backup" + str(datetime.now().strftime("%Y%m%d")), 'gztar', directorio)
copia_seguridad = "backup" + str(datetime.now().strftime("%Y%m%d")) + ".tar.gz"

# Nos conectamos al servidor FTP
ftp = ftplib.FTP()
ftp.connect("192.168.1.22",21)
ftp.sendcmd('USER Enrique')
ftp.sendcmd('PASS Arbeloa123*')
ftp.dir()
ftp.cwd('Enrique')
# Subimos el archivo al servidor
subir_archivo = open(copia_seguridad, "rb")
ftp.storbinary("STOR " + copia_seguridad, subir_archivo)
subir_archivo.close()

# Borramos el archivo de la máquina local
os.remove(copia_seguridad)

# Comprobamos la cantidad de copias subidas y eliminamos la más antigua si hay más de 10
copias_subidas = ftp.nlst()
copias_subidas.sort()
if len(copias_subidas) > 10:
    ftp.delete(copias_subidas[0])
ftp.quit

#Guardamos la dirección del remitente y el destinatario en variables
from email.message import EmailMessage
emisor='emillan1312@ieszaidinvergeles.org'
contrasena=''
receptor='gomari2100@gmail.com'
asunto='copia de seguridad del servidor'
cuerpo="Realizada con éxito"

#Enviamos el correo
email=EmailMessage()
email['Subject']=asunto
email['From']=emisor
email['To']=receptor
email.set_content(cuerpo)

contexto=ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
    smtp.login(emisor,contrasena)
    smtp.sendmail(emisor,receptor,email.as_string())

print ('El correo se ha enviado con éxito')
