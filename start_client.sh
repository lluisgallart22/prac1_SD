#!/bin/bash

echo "Introdueix el teu nom:"
read nom

python3 server/nameServer.py set '127.0.0.1' 4000 "$nom" 0

error=1
while [ $error -ne 0 ] 
do 
	echo "Escull una de les següents opcions:"
	echo "1.Connect chat"
	echo "2.Subscribe to group chat"
	echo "3.Discover chats"
	echo "4.Acces insult channel"
	echo "5.Xat privat"
	read -p "Opcio:" option
	case $option in
		"1")
			result=$(python3 server/nameServer.py get joan)
			echo "$result"
			error=0
			;;
		"2")
			echo "Que vols fer crear un nou xat Grupal o connectarte a un existent?"
			python3 discover/discoverChannel
			echo "Si vols crear un grup has de posar un nom diferents a aquets o si vols entrar a un grup sol has de escriure el nom del grup."
			read nomXat
			python3 xatGrupal/recived_logs.py $nomXat
			break
			;;
		"3")
			echo "Els grups creats son els següents:"
			python3 discover/discoverChannel
			break
			;;
		"4")
			echo "Acces al chat d'insults"
			python3 insults/insultClient.py
			break
			;;
		"5")
			echo "Acces al chat privat"
			gnome-terminal -- bash -c "python3 xatPrivat/serverXat.py"
			python3 xatPrivat/clientXat.py
			break
			;;

		*)
			echo "Aquesta opció no existeix"
			;;
	esac
done
