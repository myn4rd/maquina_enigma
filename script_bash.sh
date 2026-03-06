#!/usr/bin/env bash 

if [[ $(which python3) == "" ]]; then 
    echo "Python3 no encontrado, instalando"
    sudo apt install python3 
else 
    echo "Instalando python3-dotenv"
    sudo apt install -y python3-dotenv
fi
