path=$1

if [ -d report2pdf ]; then
	rm -r report2pdf
fi
mkdir report2pdf
cd report2pdf

cp -r ${path}/validation_report.md ${path}/figures .

# process .md
user_mail=`echo "$(getent passwd $USER)" | cut -d ':' -f 5 | sed s/','/' ('/g`
user_mail=`echo ${user_mail}")"` 

cat <<EOF > tmp.md
---
title: Validation Report
author: ${user_mail}
header-includes: |
    \usepackage[left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm]{geometry}
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \usepackage{palatino}
---

EOF
awk 'BEGIN{skip=0; counter=0}{
if($1=="<details>"){
	next
}
if($1=="[**Go"){
        next
}
if($1~"<summary><b><i>"){
	next
}
if($1=="<summary><i>" && $2=="Postprocess" && $3=="settings"){
	#print $1 $2
	skip=1
	appendix[counter] = "##"
	for(i=2;i<NF;i++){
		appendix[counter]=appendix[counter]" "$i
	}
	appendix[counter]=appendix[counter]" {.unnumbered .unlisted}"
	counter++
	next
}
if(skip==1){
	if($1=="</details>"){
		skip=0
		next
	}
	appendix[counter++]=$0""
}
if(skip==0){
	if($1=="</details>"){
		next
	}
	print $0
}
}
END{
print ""
print "# Appendix"
print ""
print ""
for(c=0; c<counter; c++){
	print appendix[c]
}
}' validation_report.md >> tmp.md

mv tmp.md validation_report.md

pandoc validation_report.md --toc -o validation_report.pdf

# process .tex
#pandoc validation_report.tex -o validation_report.pdf
