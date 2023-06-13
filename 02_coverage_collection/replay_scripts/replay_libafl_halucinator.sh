
TARGET_DIR="./armfuzz/queues"
TARGETS=(atmel_6lowpan_udp_rx atmel_6lowpan_udp_tx nxp_lwip_http p2im_controllino_slave p2im_drone samr21_http st-plc stm32_tcp_echo stm32_tcp_echo_client stm32_udp_echo stm32_udp_echo_client wycinwyc)
VALID_BB_DIR="./armfuzz/valid_bb_files"
VALID_BB_FILES=(atmel_6lowpan_udp_rx atmel_6lowpan_udp_tx nxp_lwip_http p2im_plc p2im_drone samr21_http st-plc stm32_tcp_echo stm32_tcp_echo_client stm32_udp_echo stm32_udp_echo_client wycinwyc)


for i in {0..11}; do
    for j in {0..4} ; do
        #echo "python3 eval_bbs_halucinator.py $TARGET_DIR/libAFL_halfuzz_$j/tests/${TARGETS[i]} $VALID_BB_DIR/${VALID_BB_FILES[i]}.elf_bbs.txt"
        echo "python3 eval_bbs_halucinator.py $TARGET_DIR/libAFL_halfuzz_$j/tests/${TARGETS[i]} $VALID_BB_DIR/${VALID_BB_FILES[i]}.elf_bbs.txt libafl_halucinator_${TARGETS[i]}_$j.data"
    done
done | xargs -I{} --max-procs 5 -- bash -c "{}"
