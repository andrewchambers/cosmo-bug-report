# Cosmopolitan tiny pthread investigation

A standalone C reproducer for a `SIGSYS` observed on Intel macOS 15 with
Cosmopolitan 4.0.2's tiny runtime. There is no Rust or lunacy dependency.

```sh
cosmocc -Os repro.c -o default.com
cosmocc -Os -mtiny repro.c -o tiny.com
sh ./default.com
sh ./tiny.com
```

Both programs should create and join one pthread, then exit successfully.
The worker only returns its argument. No mutex, allocation, or I/O is needed
in the test itself.

The workflow downloads the latest published toolchain from the official
`cosmocc.zip` URL, records its SHA-256 and release metadata, and runs both
variants ten times on Linux x86-64 and Intel macOS. Raw exit codes are saved
in `results.json`; a crash fails the job. Investigation results will be
recorded here after the run completes.
