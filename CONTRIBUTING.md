# Contributing

## Setup

```bash
make install   # uv sync
make hooks     # pre-commit (lint/format on commit; mypy + fast tests on push)
```

## Workflow

1. Branch from `main` (`feat/…`, `fix/…`); keep PRs focused.
2. Run `make check` before pushing; CI runs the same checks plus the full matrix.
3. Add tests with the change. Statistical tests must be seeded (use the `rng` fixture) and use
   tolerances derived from the standard error, never exact equality on simulated values.
   Mark long ones `@pytest.mark.slow`.
4. Update `CHANGELOG.md` under **Unreleased**.

## Conventions

- Formatting and linting: `ruff` (config in `pyproject.toml`). Google-style docstrings.
- Docs: the API reference is generated from docstrings, so there is nothing to write by hand for it.
  Prose pages are Markdown in `docs/` (add them to the toctree in `docs/index.md`); preview with
  `make docs-live`.
- Full type annotations; `mypy --strict` must pass.
- Dependencies: `uv add <pkg>` (runtime) or `uv add --group dev <pkg>`; commit `uv.lock`.
- New games/strategies are instantiated from Hydra configs in `conf/`; document new groups or
  options in `conf/README.md`.

## Releasing

Bump `version` in `pyproject.toml`, move the changelog entries under the new version, merge, then
tag `vX.Y.Z` and push the tag. The release workflow does the rest.
