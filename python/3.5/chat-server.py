import socket

hote = ''
port = 12800

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

connexion_avec_client, infos_connexion = connexion_principale.accept()

msg_recu = b""
msg_a_envoyer = b""
x,y = 0,0
sent = True
while msg_recu != b"fin":
	msg_a_envoyer = str(x)+" "+str(y)
	x += 10
	y += 10
	if x == 500:
		x = 0
	if y == 600:
		y = 0
	#input("> ")
	msg_a_envoyer = msg_a_envoyer.encode()
	if sent == False:
		connexion_avec_client.send(msg_a_envoyer)
		sent = True
	msg_recu = connexion_avec_client.recv(1024)
	print(msg_recu.decode())
# L'instruction ci-dessous peut lever une exception si le message
# Réceptionné comporte des accents

print("Fermeture de la connexion")
connexion_avec_client.close()
connexion_principale.close()
