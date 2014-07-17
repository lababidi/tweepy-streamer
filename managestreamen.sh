#!/bin/bash
until ./streaming.py --track "ger,fra,frager,gerfra,france,germany,bracol,colbra,bra,col,brazil,colombia,argbel,belarg,arg,argentina,belgium,belnel,nedcrc,crcned,ned,crc,nederlands,costa,worldcup,worldcup2014" --folder worldcupen --token 2 --lang "en"; do
    echo "Server 'myserver' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
