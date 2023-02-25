#!/bin/bash
#get dirctory name
func_getdirname () {
    grepresult=`grep "Organism:*" $1`
    organism_name=${grepresult/Organism: /}
    dirname=${organism_name/ /_}
    echo $dirname
}

#make dirctories based on organism name
for file in `ls ./in/*.txt`
do
dirname=$(func_getdirname $file) 
mkdir -p ./results/$dirname
done

#move .txt file to corresponding directory based on the organism name
for file in `ls ./in/*.txt`
do
dirname=$(func_getdirname $file)  
cp $file ./results/$dirname
done

#change file name
for dir in `ls ./results`
do
    for file in `ls ./results/$dir/*.txt`
    do
        gene_name=$(head -n1 $file | awk '{ print $1 }')
        txtname="$gene_name""_$(func_getdirname $file)"
        mv $file ./results/$dir/${txtname}.txt
    done
done

#writ TSV file
func_writeTsv () {
    #get new txt file name
    gene_name=$(head -n1 $1 | awk '{ print $1 }')
    grepresult=`grep "Organism:*" $1`
    organism_name=${grepresult/Organism: /}
    dirname=${organism_name/ /_}
    txtname="$gene_name""_$dirname"
    #get original txt file name
    filenametxt=${1##*/}
    filename=${filenametxt/.txt/}
    #get file length
    file_length=$(wc -l $1 | awk '{ print $1 }')
    #get gene_ID
    geneID=$(grep 'Gene ID:*' $1 | awk '{ print $3 }')
    gene_ID=${geneID/,/}
    echo $filename $txtname $file_length $gene_ID
}
#output all the information into TSV file
echo "original_name new_name file_length gene_ID" > ./results/resultstemp.tsv
for file in `ls ./in/*.txt`
do
    op=$(func_writeTsv $file)
    echo $op >> ./results/resultstemp.tsv
    #align columns with column command
    column -t ./results/resultstemp.tsv > ./results/results.tsv
done
rm ./results/resultstemp.tsv
