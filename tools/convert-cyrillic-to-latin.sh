#!/bin/bash
CYR_CAP=('А' 'Б' 'В' 'Г' 'Д' ' Е' 'Е' 'Ё' 'Ж' 'З' 'И' 'Й' 'К' 'Л' 'М' 'Н' 'О' 'П' 'Р' 
         'С' 'Т' 'У' 'Ф' 'Х' 'Ц' 'Ч' 'Ш' 'Ъ' 'Ь' 'Э' 'Ю' 'Я' 'Ў' 'Қ' 'Ғ' 'Ҳ')

LAT_CAP=('A' 'B' 'V' 'G' 'D' ' Ye' "E" 'Yo' 'J' 'Z' 'I' 'Y' 'K' 'L' 'M' 'N' 'O' 'P' 'R' 
         'S' 'T' 'U' 'F' 'X' 'C' 'Ç' 'Ş' 'ʼ' '' 'E' 'Yu' 'Ya' 'Ō' 'Q' 'Ḡ' 'H')

CYR_SML=('а' 'б' 'в' 'г' 'д' ' e' 'е' 'ё' 'ж' 'з' 'и' 'й' 'к' 'л' 'м' 'н' 'о' 'п' 'р'
         'с' 'т' 'у' 'ф' 'х' 'ц' 'ч' 'ш' 'ъ' 'ь' 'э' 'ю' 'я' 'ў' 'қ' 'ғ' 'ҳ')

LAT_SML=('a' 'b' 'v' 'g' 'd' ' ye' 'e' 'yo' 'j' 'z' 'i' 'y' 'k' 'l' 'm' 'n' 'o' 'p' 'r'
         's' 't' 'u' 'f' 'x' 'c' 'ç' 'ş' 'ʼ' '' 'e' 'yu' 'ya' 'ō' 'q' 'ḡ' 'h')

if [ -z "$1" ]; then
    echo "Please provide file to convert"
    echo "E.g.: $0 <file name>"
    exit 127 
fi

document="$1"

index=0
for letter in "${CYR_SML[@]}"; do
    sed -i "s/${letter}/${LAT_SML[$index]}/gI" ${document}
    echo "${index}: ${letter} -> ${LAT_SML[$index]}"
    index=$((${index} + 1))
done

index=0
for letter in "${CYR_CAP[@]}"; do
    sed -i "s/${letter}/${LAT_CAP[$index]}/g" ${document}
    echo "${index}: ${letter} -> ${LAT_CAP[$index]}"
    index=$((${index} + 1))
done
