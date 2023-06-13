DIR="$(dirname "$(readlink -f "$0")")"
TARGET_DIR=$DIR/fuzzware_nohal_data

N_PARALLEL_JOBS=5

TARGETS="atmel_6lowpan_udp_rx atmel_6lowpan_udp_tx nxp_lwip_http p2im_plc p2im_drone samr21_http st-plc stm32_tcp_echo_server stm32_tcp_echo_client stm32_udp_echo_server stm32_udp_echo_client wycinwyc"

# Generate stats
for t in $TARGETS; do
    for j in {0..5} ; do
        echo HAL_ENTRY_BB_FILE=$DIR/halhooks/$t.hal_hooks.txt fuzzware genstats -p $DIR/../01_fuzzing/fuzzware/firmware/$t/fuzzware-project-run-0$j --valid-bb-file $DIR/valid_bb_files/$t.elf_bbs.txt -f
    done
done |  xargs -I{} --max-procs $N_PARALLEL_JOBS -- bash -c "{}"

# Collect results
mkdir -p $TARGET_DIR

cd $DIR/../01_fuzzing/fuzzware/firmware/

for csv in `find . | grep covered_bbs_by_second_into_experiment.csv`; do
    data_name=$(echo $csv | sed 's/\/fuzzware-project-run-/_/g' | sed 's/\/stats.*/.data/g' | sed 's/\.\//fuzzware_nohal_/g')
    cp $csv $TARGET_DIR/$data_name
done
