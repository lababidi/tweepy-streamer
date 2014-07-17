#!/bin/bash
until ./streaming.py --track "ger,fra,frager,gerfra,france,germany,bracol,colbra,bra,col,brazil,colombia,argbel,belarg,arg,argentina,belgium,belnel,nedcrc,crcned,ned,crc,nederlands,costa,worldcup,worldcup2014" --folder worldcuplang --token 1 --lang "ar,nl,fr,de,es,ja,ru,sv,tr,ml,pt"; do
    echo "Server 'myserver' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
