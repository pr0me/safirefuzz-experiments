
VALID_BB_DIR="./armfuzz/valid_bb_files/"
BASE_DIR="armfuzz/crashes/rerun_queues"
TARGETS="atmel_6lowpan_udp_rx atmel_6lowpan_udp_tx nxp_lwip_http p2im_controllino_slave p2im_drone samr21_http st-plc stm32_tcp_echo stm32_tcp_echo_client stm32_udp_echo stm32_udp_echo_client wycinwyc"


for TARGET in $TARGETS; do
    for i in {0..4} ; do
        echo "python3 eval_bbs_halucinator.py $BASE_DIR/${TARGET}_$i/ $VALID_BB_DIR/${TARGET}.elf_bbs.txt safire_${TARGET}_$i.data"
    done
done | xargs -I{} --max-procs 5 -- bash -c "{}"