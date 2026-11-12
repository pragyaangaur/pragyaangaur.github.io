# NumPy Lean Check

> I modelled NumPy's integer, shape, indexing, dtype, datetime and string logic in Lean 4 and tested the model against the real library. Ask bincount to count one huge number and it returns nothing.

November 2026. Section: Maths.

## Results

- 55 bug records, 26 of them new to NumPy, with 121 properties proved and 87 refuted
- The bincount bug is filed upstream as numpy/numpy#33305

## Story

Python and Julia had already been checked against Lean models, and nobody had done it for NumPy. Fifty differential tests agree with NumPy 2.5.4 on three seeds, and every bug record comes with a reproducer that runs against the real library.

## Links

- [Project](https://github.com/pragyaangaur/NumPy-Lean-Check)
- [Article](https://pragyaangaur.dev/NumPy-Lean-Check/)
- [Issue #33305](https://github.com/numpy/numpy/issues/33305)

## See also

- [Proof by exhaustion](https://pragyaangaur.dev/work/exhaustion/index.md)
- [Cauchy-Schwarz for real powers](https://pragyaangaur.dev/work/cauchy/index.md)
- [The maximum area of the convex hull of a polyhex](https://pragyaangaur.dev/work/polyhex/index.md)

By [Pragyaan Gaur](https://pragyaangaur.dev/). The full index is at https://pragyaangaur.dev/llms.txt and https://pragyaangaur.dev/index.json.
