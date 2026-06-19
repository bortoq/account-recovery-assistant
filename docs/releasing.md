# Releasing

## Local Validation

Run the test suite before every release:

```bash
PYTHONPATH=src python3 -m pytest -v
```

## Build The Package

If `build` is installed locally:

```bash
python3 -m build
```

This should create source and wheel artifacts under `dist/`.

## Publish To PyPI

1. Bump `version` in `pyproject.toml`.
2. Update `CHANGELOG.md`.
3. Build the package.
4. Upload with your preferred PyPI publishing flow, for example `twine upload dist/*`.
5. Create a matching GitHub Release tag and reuse the changelog notes.

## First Release Notes

The first public package should position the project as:

- safety-first account recovery guidance;
- official-channel-only workflows;
- four deep initial incident families;
- local CLI and local web wizard support.
