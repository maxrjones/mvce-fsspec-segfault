# MVCE for seg fault seemingly related to fsspec

Steps:

1. Launch a compute environment using `quay.io/developmentseed/warp-resample-profiling:2024.10.02` (E.g., VEDA Hub)
2. Run any of the following to reproduce a segfault:
   - `python example-segfault-file.py`
   - `python example-segfault-s3fs.py`
3. Run any of the following to show that no segfault occurs without fsspec:
   - `python example-working.py`
