import sys
import os
import subprocess
import datetime

harness_mapping = {"6lowpan_udp_rx": "atmel_6lowpan_udp_rx/atmel_6lowpan_udp_rx.yml", "6lowpan_udp_tx": "atmel_6lowpan_udp_tx/atmel_6lowpan_udp_tx.yml", "p2im_plc": "p2im_controllino_slave/p2im_controllino_slave.yml", "samr21": "samr21_http/samr21_http_eth.yml", "wycinwyc": "wycinwyc/expat_panda.yml", "p2im_drone": "p2im_drone/p2im_drone.yml", "nxp_http": "nxp_lwip_http/nxp_lwip_http.yml", "stm32_tcp_echo_client": "stm32_tcp_echo_client/stm32_tcp_echo_client.yml", "stm32_tcp_echo_server": "stm32_tcp_echo/stm32_tcp_echo_server.yml", "stm32_udp_echo_client": "stm32_udp_echo_client/stm32_udp_echo_client.yml", "stm32_udp_echo_server": "stm32_udp_echo/stm32_udp_echo_server.yml", "st_plc": "st-plc/st-plc.yml"}

harness_mapping["nxp_lwip_http"] = "nxp_lwip_http/nxp_lwip_http.yml"
harness_mapping["p2im_controllino_slave"] = "p2im_controllino_slave/p2im_controllino_slave.yml"
harness_mapping["st-plc"] = "st-plc/st-plc.yml"
harness_mapping["stm32_tcp_echo"] = "stm32_tcp_echo/stm32_tcp_echo_server.yml"
harness_mapping["stm32_udp_echo"] = "stm32_udp_echo/stm32_udp_echo_server.yml"

def process(path, valid_bbs_file):
    with open(valid_bbs_file, 'r') as f:
        valid_bbs = f.readlines()
    valid_bbs = set([int(bb, 16) for bb in valid_bbs])

    if "libafl" in path.lower():
        dir = os.fsencode("./" + path + "/out")
    elif "hal-fuzz" in path:
        dir = os.fsencode("./" + path + "/output/queue")    
    else:
        dir = os.fsencode("./" + path + "/queue")

    time_to_filename = {}
    time_to_num_bb = {}
    sorted = []
    unique_block_addr = set()

    harness = "/workspaces/hal-fuzz/tests/"
    for k, v in harness_mapping.items():
        #if k in dir.decode().split('/'):
        if k in dir.decode():
            harness += v
    print(harness)


    print("[*] Processing Files in {}".format(dir))
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if "hal-fuzz" in path and not "libafl" in path:
            input_id = filename.split(',')[0][-4:]
            while input_id.startswith('0'):
                input_id = input_id[1:]
            try:
                input_id = int(input_id)
            except:
                continue

            i = 0 
            timestamp = ''
            while timestamp == '':
                timestamp = subprocess.check_output(["awk", "-F", ",", "$4 ~ /%d/ { print $0; exit }" % (input_id + i), "../plot_data"], cwd=dir).decode().split(',')[0]
                i += 1

            sorted.append(timestamp)
            time_to_filename[timestamp] = filename
        else:
            if filename != "stat.log" and filename != "unique_bbs.out":
                timestamp = subprocess.check_output(["grep", filename, "-A", "4", "stat.log"], cwd=dir).split(b"Access: ")[-1].strip(b'\n').decode()
                sorted.append(timestamp)
                time_to_filename[timestamp] = filename
    
    print(time_to_filename)
    sorted.sort()
    i = 0
    exceptions = 0
    for t in sorted:
        file = time_to_filename[t]
        cmd = ["timeout", "-s", "1", "5", "python3", "-m", "hal_fuzz.harness", "-c", harness, file]
        print("[*] Executing Harness: {}".format(cmd))
        try:
            result = subprocess.run(cmd, cwd=dir, stdout=subprocess.PIPE, timeout=5)
        except subprocess.TimeoutExpired:
            pass
        with open(dir.decode() + "/unique_bbs.out", "r") as output:
            try:
                unique_block_addr |= eval(output.read())
                unique_block_addr &= valid_bbs
            except:
                exceptions += 1
                continue
        

        time_to_num_bb[t] = len(unique_block_addr)
        print(exceptions)
        i += 1
        if i % 8 == 0:
            print(time_to_num_bb)

    return time_to_num_bb

if __name__ == "__main__":
    path = sys.argv[1]
    valid_bbs_file = sys.argv[2]
    outname = sys.argv[3]
    out = process(path, valid_bbs_file)
    testname = [p for p in path.split('/') if p != ''][-1]
    with open(outname, "w+") as f:
        f.write(repr(out))
    