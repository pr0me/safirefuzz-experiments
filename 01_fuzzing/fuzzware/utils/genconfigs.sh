for i in `ls`; do cd $i; fuzzware genconfig $i.elf; cd ..; done

# Unfortunately, the base address of the samr21_http firmware is wrongly calculated by fuzzware's genconfig utilities.
# Hence, we resort to manually fix it
echo "Fixing up config for samr21_http"
sed -i 's/-0xf000/0x00/g' ./samr21_http/config.yml

