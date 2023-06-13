TARGET_LIST="atmel_6lowpan_udp_rx atmel_6lowpan_udp_tx nxp_lwip_http samr21_http p2im_drone wycinwyc p2im_plc_slave st-plc stm32_tcp_echo_server stm32_tcp_echo_client stm32_udp_echo_client stm32_udp_echo_server"

echo "Target, exec/s"
for t in ${TARGET_LIST}; do
    for i in {1..5}; do
        cd ./firmware/$t/fuzzware-project-run-0$i/
        n_execs=$(grep -ri execs_done | cut -d ':' -f 3 | paste -sd+ - | bc)
        printf "$t #$(($i-1)), %.1f\n" $((n_execs/86400))e-1
        cd ../../../
    done
    echo
done
