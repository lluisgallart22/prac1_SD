#!/bin/bash
error=1
while [ $error -ne 0 ] 
do 
	echo "Escull una de les següents opcions:"
	echo "1.Connect chat"
	echo "2.Subscribe to group chat"
	echo "3.Discover chats"
	echo "4.Acces insult channel"
	read -p "Opcio:" option
	case $option in
		"1")
			result=$(python3 getNameServer.py ConnectChat)
			echo "$result"
			error=0
			;;
		"2")
			echo "Nom del xat:"
			read -p nomXat
			python3 recived_logs.py $nomXat
			error=0
			;;
		"3")
			#script3
			error=0
			;;
		"4")
			#script4
			error=0
			;;
		*)
			echo "Aquesta opció no existeix"
			;;
	esac
done
