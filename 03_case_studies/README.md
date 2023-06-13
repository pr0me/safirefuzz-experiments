# Case Studies

Besides the previously explored and fuzzed targets we used for evaluation and comparison against other state-of-the-art
firmware fuzzing frameworks, we also rehosted and fuzzed two novel targets:

- STM32 Sine: open-source firmware for electric motor inverters (https://github.com/jsphuebner/stm32-sine)
- JPEG Decoder: STM32 example firmware for image processing (https://github.com/STMicroelectronics/STM32CubeF4/tree/master/Projects/STM324x9I_EVAL/Applications/LibJPEG/LibJPEG_Decoding)

The compiled binaries can be found in `../00_firmware`.

We identified three previously unknown bugs:
- **STM32 Sine**: 
    - we explore a substantial part of the terminal interface which parses and processes various commands to change hardware-internal parameters via CAN bus communication. 
    SAFIREFUZZ finds a crash related to updating certain parameter enumerations in the CAN configuration. 
    An interface ID is retrieved from memory and used as an offset into memory. 
    Corrupting this value leads to arbitrary memory writes. 
    We could not confirm whether this crash is a true positive, as part of its root cause lies in the hardware configuration, which may be reported wrongly by our HAL hooks.
- **JPEG Decoder**: 
    - a segmentation fault: a critical error routine that, instead of terminating the program after beginning to parse a corrupted input image, falls through silently. 
    Subsequently, no checks are in place to avoid accessing and dereferencing pointers in uninitialized structs in memory.
    - Output buffers in the color conversion function have hard-coded sizes but the faulty routine uses the decoded image’s width to iterate over scanlines and write to the buffer, heavily exceeding the stack-located buffer’s limits.

We disclosed the previously unknown vulnerabilities to the respective maintainers.

The crashing inputs are provided in this directory and can be reproduced as follows:
```
cd ../01_fuzzing/
./safirefuzz_target.py libjpeg -i ../03_case_studies/crashing_inputs/jpeg_decoder/buffer_overflow_unchecked_img_size
```
Note: for the second bug in the JPEG Decoder to trigger, you need to remove line 44 in `../01_fuzzing/SAFIREFUZZ/src/harness/libjpeg_decoding.rs`.  
For exploration, we let the engine exit upon hitting the faulty error routine as otherwise we would observe a _lot_ of crashes, slowing down fuzzing.