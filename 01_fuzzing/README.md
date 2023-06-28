# Fuzzing

This directory contains everything needed to run SAFIREFUZZ and replicate our experiments 
including comparisons against other approaches:

- Frameworks
    - code, patches and build/run scripts for all evaluated rehosting/fuzzing frameworks
- Firmware
    - firmware blobs for the evaluated targets 
    - compiled for ARMv7-M
- Seeds
    - fuzzing seeds as used during evaluation

Before fuzzing, make sure your system is configured properly (run as root):
```bash
echo core >/proc/sys/kernel/core_pattern
cd /sys/devices/system/cpu
echo performance | tee cpu*/cpufreq/scaling_governor

./SAFIREFUZZ/prepare_sys.sh
```

## Frameworks

Clone all linked repositories by running
```
git submodule update --init --recursive
```

### SAFIREFUZZ
First, install SAFIREFUZZ as explained in the repository.

Afterwards you can run the following script to automatically re-compile our framework for the specified target harness and start fuzzing:
```
./safirefuzz_target.py wycinwyc
```
This will **only work** on a CPU supporting the ARMv7-M instruction set, e.g., a Cortex-A72 found in Raspberry Pi 4.

### HALucinator
For HALucinator, we include the fuzzing-optimized version `hal-fuzz`.  
We provide a patch, fixing one bug and configuring run scripts in a way that they will directly fuzz the target.

First, apply this patch by running:
```
cd hal-fuzz && git apply --reject --whitespace=fix ../halucinator-patch.diff
```

Then, install HALucinator (needs sudo):
```
mkvirtualenv -p /usr/bin/python3 halfuzz
./setup.sh
```

In order start the fuzzing campaign for a specific target, use the provided run scripts within an activated python virtual environment:
```
source ~/.virtualenvs/halfuzz/bin/activate
timeout 24h ./test_p2im_drone.sh
```

Target name disambiguation:
| Name in Paper | hal-fuzz script |
|---|---|
| NXP HTTP | test_nxp_lwip_http.sh |
| P2IM PLC | test_p2im_controllino.sh |
| SAMR21 HTTP  | test_samr21_http_eth.sh |

Use the *_fuzz.sh scripts where available, otherwise the scripts should be patched accordingly to spin up AFL.

### HALucinator - libAFL
For building, the LibAFL version from the SAFIREFUZZ main repository is used.  
Apply the provided LibAFL patches:
```
cd ./SAFIREFUZZ/LibAFL/ && git apply ../../forkserver_libAFL/libAFL_patch.diff
```
Build the forkserver for your current target:
```
cd ./forkserver_libAFL
cargo build --release
```
OR
```
cargo build --release --target armv7-unknown-linux-gnueabihf
```

You can run hal-fuzz harnesses from their respective directories like this, replacing the default AFL with a libAFL server (make sure you use the virtualenv with the hal-fuzz installation):
```
cd hal-fuzz/tests/st-plc
../../../forkserver_libAFL/target/armv7-unknown-linux-gnueabihf/release/forkserver_ondisk ~/.virtualenvs/halfuzz/bin/python3 inputs -m hal_fuzz.harness -n --native-lib=../../hal_fuzz/hal_fuzz/native/native_hooks.so -c st-plc.yml @@
```

### Fuzzware
For details regarding the Fuzzware setup, please have a look at the [dedicated README](./fuzzware/README.md).