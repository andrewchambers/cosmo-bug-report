# Cosmopolitan tiny pthread investigation

A minimal pthread program crashes with `SIGSYS` on Intel macOS 15.7.9 when
built with Cosmopolitan's tiny runtime. The default runtime succeeds.
The minimal test passes when built from current upstream master.
There is no Rust or lunacy dependency.

## Reproduce

With `cosmocc` on `PATH`:

```sh
cosmocc -Os repro.c -o default.com
cosmocc -Os -mtiny repro.c -o tiny.com
sh ./default.com
sh ./tiny.com
```

[`repro.c`](repro.c) is 13 lines: create one pthread, return its argument, and
join it. Both executables should exit with status 0. No mutex, explicit
allocation, or I/O is needed in the test.

## Latest published toolchain

Checked on 2026-09-05 using the official
[latest toolchain archive](https://cosmo.zip/pub/cosmocc/cosmocc.zip).
The latest published release is still **4.0.2**, with GCC 14.1.0.
The archive SHA-256 is:

```text
85b8c37a406d862e656ad4ec14be9f6ce474c1b436b9615e91a55208aced3f44
```

| Host | Default runtime | Tiny runtime |
| --- | --- | --- |
| Linux x86-64 | 10/10 exit 0 | 10/10 exit 0 |
| macOS 15.7.9 Intel | 10/10 exit 0 | 10/10 `SIGSYS` |

Python reports the terminating signal as exit code `-12` on macOS.
See the [CI run](https://github.com/andrewchambers/cosmo-bug-report/actions/runs/33944172105)
and [saved results](evidence/release.json).

## Current upstream source

Also tested upstream master at
[`3293fad0a9eac7865c019be98fb993eeb933405e`](https://github.com/jart/cosmopolitan/commit/3293fad0a9eac7865c019be98fb993eeb933405e),
the latest commit when checked on 2026-09-05.

| Host | Default runtime | Tiny runtime |
| --- | --- | --- |
| Linux x86-64 | 10/10 exit 0 | 10/10 exit 0 |
| macOS 15.7.9 Intel | 10/10 exit 0 | 10/10 exit 0 |

See the [source-build CI run](https://github.com/andrewchambers/cosmo-bug-report/actions/runs/33944255524)
and [saved results](evidence/head.json). These use upstream's Makefile and
compiler bootstrap, as described below. The failure is confirmed with the
latest published toolchain but is **not reproduced in this current source
build**. No particular fix commit or root cause has been identified.

## Investigation workflows

[Reproduce](.github/workflows/reproduce.yml) downloads the latest published
toolchain, records its checksum and release metadata, and builds directly
with `cosmocc` on Linux and Intel macOS. Each executable runs ten times.
Crashes fail the job; results and binaries are uploaded even on failure.

[Current upstream source](.github/workflows/head.yml) is manually dispatched.
It checks out `jart/cosmopolitan` master, records the exact commit, and uses
upstream's Makefile to rebuild the default and tiny runtimes for the same
program. It runs the resulting binaries on Linux and Intel macOS. The
upstream Makefile provisions its own pinned compiler bootstrap.

Each trial executes a fresh copy because some upstream APE build modes rewrite
their executable header. The binaries distributed between hosts stay intact.
