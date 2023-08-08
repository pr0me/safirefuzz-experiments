# SAFIREFUZZ Experiments
[![DOI](https://zenodo.org/badge/653182569.svg)](https://zenodo.org/badge/latestdoi/653182569)

<br />

This repository contains documentation, scripts and raw data for the artifact evaluation of the USENIX `23 paper 
"Forming Faster Firmware Fuzzers".

For more details regarding our work, have a look at the main repository:  
https://github.com/pr0me/SAFIREFUZZ

This repository is structured as follows:
- Firmware: 
    - The firmware used in the evaluation of this paper
- Fuzzing: 
    - setup and build scripts / documentation for the frameworks we evaluated our approach against
    - includes firmware binaries and initial fuzzing seeds
- Coverage Collection
    - setup used to re-run fuzzing queues to collect detailed coverage information
- Case Studies
    -  information regarding the two novel targets we investigated
- Eval Data
    - raw data collected during our evaluation, matching the results reported in the paper

<br />
A note on the sequence of experiments:  

Overall, it is possible to either first run fuzzing for all targets and collect coverage by replaying the queues afterwards, or fuzz, collect, fuzz, collect...  
But there are a couple of things to pay attention to:
1. Always make sure to make backups of your fuzzing queues. 
Especially for `safirefuzz_target.py`, output directories might get re-used.
2. The cov collection script for SAFIREFUZZ and hal-fuzz (`eval_bbs_halucinator.py`) replays one target at a time and takes input and output paths as arguments, so it should be straight-forward to parallelize things.   
If you wish, you can also adapt our [scripts](02_coverage_collection/replay_scripts) to this end.
3. If you switch between fuzzing and coverage collection, remember to apply and [revert](https://github.com/pr0me/safirefuzz-experiments/blob/d85d406597842b7fdebe427e82f781e7d366046b/01_fuzzing/README.md?plain=1#L55) the different sets of HALucinator patches for fuzzing and replaying or make a local copy of the hal-fuzz directory for both use cases.

Using coverage collected on your own or our [original data](04_eval_data/coverage/bb_mann_whitney.ipynb), you can then proceed to replicate our results with our [statistics]() and [plotting scripts](04_eval_data/coverage/gen_fig3.ipynb).



## Citation
```
@inproceedings{seidel2023ffff,
  title={Forming Faster Firmware Fuzzers},
  author={Seidel, Lukas and Maier, Dominik and Muench, Marius},
  booktitle={USENIX 2023},
  year={2023}
}
```
