#!/usr/bin/env python3

import sys
import os
import subprocess


TARGETS = {'6lowpan_rx': {'harness': "atmel_6lowpan_rx", 'bin': "../00_firmware/atmel_6lowpan_udp_rx.bin"},
            '6lowpan_tx': {'harness': "atmel_6lowpan_tx", 'bin': "../00_firmware/atmel_6lowpan_udp_tx.bin"},
            'nxp_http': {'harness': "nxp_http", 'bin': "../00_firmware/nxp_lwip_http.bin"},
            'samr21_http': {'harness': "atmel_http", 'bin': "../00_firmware/samr21_http.bin"},
            'p2im_plc': {'harness': "p2im_plc", 'bin': "../00_firmware/p2im_plc.bin"},
            'p2im_drone': {'harness': "p2im_drone", 'bin': "../00_firmware/p2im_drone.bin"},
            'stm_plc': {'harness': "st_plc", 'bin': "../00_firmware/st-plc.bin"},
            'wycinwyc': {'harness': "wycinwyc", 'bin': "../00_firmware/wycinwyc.bin"},
            'tcp_echo_client': {'harness': "stm32_tcp_echo_client", 'bin': "../00_firmware/stm32_tcp_echo_client.bin"},
            'tcp_echo_server': {'harness': "stm32_tcp_echo_server", 'bin': "../00_firmware/stm32_tcp_echo_server.bin"},
            'udp_echo_client': {'harness': "stm32_udp_echo_client", 'bin': "../00_firmware/stm32_udp_echo_client.bin"},
            'udp_echo_server': {'harness': "stm32_udp_echo_server", 'bin': "../00_firmware/stm32_udp_echo_server.bin"},
            'libjpeg': {'harness': "libjpeg_decoding", 'bin': "../00_firmware/LibJPEG_Decoding.bin"},
            'stm32_sine': {'harness': "stm32_sine", 'bin': "../00_firmware/stm32_sine.bin"},
            }


if __name__=="__main__":
    if len(sys.argv) == 1:
        print("Please provide a target identifier to fuzz.\nSee available identifiers with '-h'")
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Start fuzzing with `-f` (default) or execute single input with `-i`")
        print("Available target identifiers:")
        for t in TARGETS.keys():
            print(t)
    else:
        target = sys.argv[1]
        if target not in TARGETS.keys():
            print("Not a valid target identifier.")
            exit()

        # replace import in engine.rs
        harness_import = f"use crate::harness::{TARGETS[target]['harness']} as harness;"
        os.system('sed -i "1s/.*/{}/" ./SAFIREFUZZ/src/engine.rs'.format(harness_import))

        # re-compile
        os.system("cd SAFIREFUZZ && cargo build --release --target armv7-unknown-linux-gnueabihf")

        # start execution
        if len(sys.argv) > 2 and sys.argv[2] == '-i':
            input_file = sys.argv[3]
            # cmd = ["./SAFIREFUZZ/target/armv7-unknown-linux-gnueabihf/release/safirefuzz", "-b", f"{TARGETS[target]['bin']}", "-i" f"{input_file}"]
            cmd = f"./SAFIREFUZZ/target/armv7-unknown-linux-gnueabihf/release/safirefuzz -b {TARGETS[target]['bin']} -i {input_file}"
        else:
            # cmd = ["timeout", "24h", "./SAFIREFUZZ/target/armv7-unknown-linux-gnueabihf/release/safirefuzz", "-b", f"{TARGETS[target]['bin']}", "-i", f"seeds/{TARGETS[target]['harness']}", "-f", "-c", "2"]
            cmd = f"timeout 24h ./SAFIREFUZZ/target/armv7-unknown-linux-gnueabihf/release/safirefuzz -b {TARGETS[target]['bin']} -i seeds/{TARGETS[target]['harness']} -f -c 2"

        print(cmd)
        try:
            subprocess.call(cmd, stdout=sys.stdout, stderr=subprocess.STDOUT, shell=True)
        except:
            os.system("killall safirefuzz")
