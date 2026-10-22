"""Measure CIFTI-2 scalar-index agreement with the Python-int reference."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["before", "after"])
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    np.random.seed(0)
    import nibabel.cifti2.cifti2_axes as axes
    from nibabel.cifti2.tests.test_axes import get_axes

    index_types = [int, np.int8, np.int16, np.int32, np.int64,
                   np.uint8, np.uint16, np.uint32, np.uint64]
    fixtures = [*get_axes(), axes.SeriesAxis(-1000, 1000, 3)]
    rows = []
    for fixture, axis in enumerate(fixtures):
        for index_type in index_types:
            start = 0 if np.issubdtype(index_type, np.unsignedinteger) else -len(axis)
            for index in range(start, len(axis)):
                error = None
                try:
                    np.testing.assert_equal(axis[index_type(index)], axis[index])
                except Exception as exc:
                    error = f"{type(exc).__name__}: {exc}"
                rows.append({"axis": type(axis).__name__, "fixture": fixture,
                             "index_type": index_type.__name__, "index": index,
                             "passed": error is None, "error": error})
    result = {"phase": args.phase, "python": platform.python_version(),
              "numpy": np.__version__,
              "source_sha256": hashlib.sha256(Path(axes.__file__).read_bytes()).hexdigest(),
              "rows": rows}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"{args.phase}: {sum(row['passed'] for row in rows)}/{len(rows)} matching results")


if __name__ == "__main__":
    main()
