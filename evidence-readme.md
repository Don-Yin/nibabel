# CIFTI-2 integer-indexing comparison

Measured on Python 3.14.3 and NumPy 2.4.3.

- Before: `fdacbf05c15f06125a481c3345a5de55a32f9ba2`
- After: `a2d9c2473f10fbaa5b1f620f5c0d6b9788d67515`
- The probe exercises the existing axis fixtures plus `SeriesAxis(-1000, 1000, 3)`.
- Eight NumPy integer types (`int8`, `int16`, `int32`, `int64`, and their unsigned counterparts) are compared with Python `int` at every valid nonnegative index, and every valid negative index for signed types.
- Across all five axis classes, NumPy-index results agree with the Python-int reference in 0/540 comparisons before the fix and 540/540 afterward. The Python-int controls pass 90/90 comparisons in both versions.
- These are functional regression measurements on synthetic fixtures, not performance measurements or clinical data.

The figure reads the recorded values in `before.json` and `after.json`. The JSON files also record a SHA-256 hash of the measured `cifti2_axes.py` source. `measure-indexing.py` produces the records when run with the corresponding checkout on `PYTHONPATH`, for example:

```sh
PYTHONPATH=/path/to/nibabel python measure-indexing.py before before.json
```

`indexing-evidence.png` is a 16 cm, 420 dpi export.
