# SAFIREFUZZ Experiments

This repository contains documentation, scripts and raw data for the artifact evaluation of the USENIX `23 paper 
"Forming Faster Firmware Fuzzers".

It is structured as follows:
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

For more details regarding our work, have a look at the main repository:  
https://github.com/pr0me/SAFIREFUZZ

## Citation
```
@inproceedings{seidel2023ffff,
  title={Forming Faster Firmware Fuzzers},
  author={Seidel, Lukas and Maier, Dominik and Muench, Marius},
  booktitle={USENIX 2023},
  year={2023}
}
```
