# Simple Forkserver Fuzzer for SAFIREFUZZ Experiments

This is based on the `forkserver_simple` example fuzzer from the LibAFL repository.
## Usage
**IMPORTANT:** 
You need to apply the provided .diff file to LibAFL in order to compile this project.  
See the main README in `01_fuzzing` for details. 

You can build this example by `cargo build --release`.

## Run
After you build it you can run **hal-fuzz** harnesses from their respective directories like this:
```
/path/to/forkserver_ondisk ~/.virtualenvs/halfuzz/bin/python3 inputs -m hal_fuzz.harness -n --native-lib=../../hal_fuzz/hal_fuzz/native/native_hooks.so -c st-plc.yml @@
```

## Configuration Details
This forkserver uses the same fuzzer configurations as used in SAFIREFUZZ,
i.e., same mutation strategies and interestingness criteria, on-disk corpora etc. 