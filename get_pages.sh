#!/bin/bash

mkdir out
mkdir out/raw
mkdir out/about


function curlget(){
    echo "curlget $@"
    command curl "$@"
}


cat vloggers.txt | while read line; do

    page1=http://www.youtube.com/$line
    page2=http://www.youtube.com/user/$line/about

    curlget -s $page1 -o out/raw/$line.html
    curlget -s $page2 -o out/about/$line.html

done

