#example use:
#./find.ps1 C:\Users\rgoodeve\WSL\Notes\* "CS Gold"
#replace "CS Gold" with the desired regex wrapped in ""
#accepts a wildcarded directory and a regex string to match
#produces a find.txt in the provided directory

$dir = $args[0]
$match = $args[1]
$outdir = $dir.substring(0,$dir.length-1)
start-transcript -path $outdir\find.txt -append
select-string -path $dir -pattern $match -context 1
stop-transcript