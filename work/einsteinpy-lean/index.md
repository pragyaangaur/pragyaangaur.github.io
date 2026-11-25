# EinsteinPy Lean Check

> I modelled all of einsteinpy, the Python library for general relativity, in Lean 4 on top of Physlib and tested it against the real library. Ask it how big the Sun would be as a black hole and it says 10⁻²⁷ metres.

November 2026. Section: Maths.

## Results

- 33 bug records, 24 of them new to einsteinpy, with 173 properties proved and 47 refuted
- The findings are raised upstream as einsteinpy/einsteinpy#712

## Story

After NumPy I wanted to try the same method on a physics library, with Physlib as the reference for the physics. Twenty differential tests agree with einsteinpy on 2.9 million cases, and the Lean proofs also check that my own fixes for lorentz_transform and the 4-momentum are right.

## Links

- [Project](https://github.com/pragyaangaur/EinsteinPy-Lean-Check)
- [Issue #712](https://github.com/einsteinpy/einsteinpy/issues/712)

## See also

- [NumPy Lean Check](https://pragyaangaur.dev/work/numpy-lean/index.md)
- [EinsteinPy](https://pragyaangaur.dev/work/einsteinpy/index.md)
- [Magnus turning invariants](https://pragyaangaur.dev/work/magnus/index.md)

By [Pragyaan Gaur](https://pragyaangaur.dev/). The full index is at https://pragyaangaur.dev/llms.txt and https://pragyaangaur.dev/index.json.
