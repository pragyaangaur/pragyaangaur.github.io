# Heliox

> I rebuilt the core of SunPy from scratch, then moved it into Rust. Where the Sun runs slow, Rust takes over.

November 2026. Section: The Sun.

## Results

- Kernels for other sunpy packages, up to 390x faster and bit-identical to the original

## Story

Heliox began as SunPy rebuilt offline to see how a solar toolkit fits together. In November 2026 its core moved into a Rust crate, with every ported function checked against the Python it replaced. A separate package then took on slow functions from other sunpy packages, and the sunkit-image one runs about 390 times faster on a real velocity field.

## Links

- [Project](https://github.com/pragyaangaur/Heliox)

## See also

- [SunPy](https://pragyaangaur.dev/work/sunpy/index.md)
- [Magnetic limb-darkening audit](https://pragyaangaur.dev/work/limb-audit/index.md)
- [Sunion](https://pragyaangaur.dev/work/sunion/index.md)

By [Pragyaan Gaur](https://pragyaangaur.dev/). The full index is at https://pragyaangaur.dev/llms.txt and https://pragyaangaur.dev/index.json.
