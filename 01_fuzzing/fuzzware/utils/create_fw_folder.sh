for i in `ls`; do mkdir $(echo ${i%.*}); mv $i $(echo ${i%.*}); done 2>/dev/null
