#!/bin/bash
Files="in/*"
Folder="out/"
if [ ! -d Folder ]
then
    $(mkdir Folder)
fi
$(touch out/summary.tsv)
for f in $Files
do
    echo "reading $f"
    desc=$(head -n 1 $f)
    echo $desc
    id=$(grep "Gene ID: [0-9]*," $f | cut -d , -f 1)
    echo $id
    organism=$(grep "organism:" $f | cut -d : -f 2)
    echo $organism
    size=$(cat $f | wc -1)
    echo $size

    echo -e "$f\t$id\t$size\t$desc\t$organism">> "Folder"/summary.tsv
    organism=${organism// /_}
    orgFolder="$Folder/$organism"
    if[ ! -d $orgFolder ]
    then
        mkdir "$Folder/$organism"
    fi
    cp "$f" "$Floder/$organism/$desc".gb
done
