#!/bin/bash

fitxerPorts="portsDisp.yaml"

if [[ ! -f "$fitxerPorts" ]]; then
    echo "No es pot realitzar cap connexió"
    exit 0
fi

primer=$(grep -oP '^\s*-\s*\K\d+' "$fitxerPorts" | head -n 1)

if [[ -z "$primer" ]]; then
    echo "No hi ha ports disponibles"
    exit 0
fi

sed -i '0,/- '"$primer"'/d' "$fitxerPorts"

echo "Introdueix el teu nom:"
read nom

python3 server/nameServer.py set '127.0.0.1' $primer $nom 0

error=1
while [ $error -ne 0 ]; do
    echo "Escull una de les següents opcions:"
    echo "1. Connect chat"
    echo "2. Subscribe to group chat"
    echo "3. Discover chats"
    echo "4. Acces insult channel"
    echo "5. Xat privat"
    echo "6. Contingut REDIS"
    read -p "Opcio: " option
    case $option in
        "1")
            echo "Et vols connectar a un xat privat o a un grupal?"
            echo "Per connectar-te a un xat privat posa 0"
            echo "Per connectar-te a un xat grupal posa 1"
            read num
            if [ $num -eq 0 ]; then
                python3 xatPrivat/serverClient.py --sender $nom --port $primer
            elif [ $num -eq 1 ]; then
                echo "Proporciona el nom del xat grupal"
                echo "En el cas de que el nom proporcionat no es trobi al servidor es crearà un de nou"
                read nomXatGrupal
                echo $nomXatGrupal
            fi
            ;;
        "2")
            echo "Proporciona el nom del xat grupal"
            echo "En el cas de que el nom proporcionat no es trobi al servidor es crearà un de nou"
            read nomXat
            python3 xatGrupal/recived_logs.py $nomXat
            ;;
        "3")
            echo "Els grups creats son els següents:"
            python3 discover/discoverChannel.py
            ;;
        "4")
            echo "Acces al chat d'insults"
            python3 insults/insultClient.py
            ;;
        "5")
            echo "Acces al chat privat"
            python3 xatPrivat/serverXat.py
            ;;
        "6")
            echo "Contingut REDIS"
            ./redis.sh
            ;;
        *)
            echo "Aquesta opció no existeix"
            ;;
    esac
done
