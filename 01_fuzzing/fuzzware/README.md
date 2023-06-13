# Fuzzware for SAFIREFUZZ Experiments

During our experiments, we used fuzzware's local build on an x86_64 ubuntu 18.04 server machine.

### Installing Fuzzware

Assuming you have all submodules checked out, please apply the SAFIREFUZZ specific modifications first.
They do not affect the fuzzing logic, but enable collection of coverage without HAL functionality and overwriting of traces (to avoid spurios data from prior runs).

```shell
cd fuzzware/emulator && git apply ../../emulator_allow_disable_hal_trace.diff && cd -
cd fuzzware/pipeline && git apply ../../pipeline_force_overwrite.diff && cd -
```

Afterwards, build and install fuzzware using the scripts provided by fuzzware:
```shell
cd fuzzware && ./install_local.sh
```

This may not work out-of-the-box for every system, but fuzzware's error are usually descriptive and may enable to fix encountered issues.

After successful installation, change to the fuzzware virtual environment, which is considered to be activated for the rest of this readme.

```shell
workon fuzzware
```

## Setting up firmware

Fuzzware requires configuration files and our setup prefers individual subdirectories for each sample.
Easiest is to copy the firmware directory (to not interfere with other experiments) and use the provided scripts to first create one subdirectory per sample, and then create one config per subdirectory.

```shell
cp -r ../../00_firmware ./firmware
cd ./firmware
../utils/create_fw_folder.sh
../utils/genconfigs.sh
```

## Running experiments

After this setup, we can run the actual experiments! For this, use the `run_experiment.sh` script, which calls `run_targets.sh` internally.
Both of these scripts are modified versions of the according scripts of the [fuzzware-experiments](https://github.com/fuzzware-fuzzer/fuzzware-experiments/tree/main/02-comparison-with-state-of-the-art) repository.
As such, comments and instructions embedded in these scripts may refer to the original fuzzware experiments, rather than the ones carried out for SAFIREFUZZ.

```shell
./run_experiment.sh
```

Note that you can adjust the amount of cores allocated to the experiments and number of repitions by passing them as additional arguments to the script:
```shell
./run_experiment.sh 10 5 # Example setup: 10 available cores and 5 repititions
```

## Data processing

After the experiments, different statistics about the different runs can be collected---most importantly, executions per seconds.
To assess the execution per seconds, please you the `collect_execs.sh` script, for collecting coverage, please refer to the [README](../../02_coverage_collection/README.md) in the `02_coverage_collection` subdirectory.
