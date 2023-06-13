#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"

TARGET_LIST="firmware/atmel_6lowpan_udp_rx firmware/atmel_6lowpan_udp_tx firmware/nxp_lwip_http firmware/samr21_http firmware/p2im_drone firmware/wycinwyc firmware/p2im_plc firmware/st-plc firmware/stm32_tcp_echo_server firmware/stm32_tcp_echo_client firmware/stm32_udp_echo_client firmware/stm32_udp_echo_server"
FUZZING_RUNTIME=24:00:00

if [ $# -ge 1 ]; then
    NUM_PARALLEL_INSTANCES="$1"
else
    # Experiment default: No parallelization
    NUM_PARALLEL_INSTANCES=1
fi

if [ $# -ge 2 ]; then
    EXPERIMENT_REPETITION_COUNT="$2"
else
    # Experiment default: 5 repetitions
    EXPERIMENT_REPETITION_COUNT=5
fi

# Default sequential config (60 days of time): 5 repetitions, 12 targets, with modeling, no parallelization
SKIP_NON_MODELING=1

# For a more lightweight version of the experiment, we can run everything a single time, and possibly run multiple experiments in parallel
# FUZZING_RUNTIME=24:00:00
# EXPERIMENT_REPETITION_COUNT=1
# NUM_PARALLEL_INSTANCES=2
# SKIP_NON_MODELING=1

fuzzware checkenv -n $NUM_PARALLEL_INSTANCES || { echo "Error during initial sanity checks. Please fix according to debug output."; exit 1; }

echo "CAUTION: Without modification, this will take a whopping 60 days to complete. This is the case as 12*5 (targets*repetitions) = 60 24-hour fuzzing experiments are executed."
echo "This is a wrapper around run_targets.sh, which you can use directly to parallelize execution and split runs of different targets to different machines to reduce the overall runtime."
echo $NUM_PARALLEL_INSTANCES

# Run all targets with modeling
$DIR/run_targets.sh 1 $EXPERIMENT_REPETITION_COUNT $NUM_PARALLEL_INSTANCES $FUZZING_RUNTIME $TARGET_LIST

if [ $SKIP_NON_MODELING -ne 1 ]; then
    # Run all targets without modeling
    $DIR/run_targets.sh 0 $EXPERIMENT_REPETITION_COUNT $NUM_PARALLEL_INSTANCES $FUZZING_RUNTIME $TARGET_LIST
fi