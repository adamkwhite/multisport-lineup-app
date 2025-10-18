# Pre-Commit Hooks

This project uses the [pre-commit](https://pre-commit.com/) framework to run code quality checks before each commit.

## History

**Note:** Previously, this project used a legacy custom pre-commit hook that checked for tools in the global PATH. This has been removed in favor of the official pre-commit framework, which properly detects tools in the virtual environment.

## What Gets Checked

Every commit automatically runs:

1. **Black** - Code formatting (Python)
2. **isort** - Import sorting (Python)
3. **Flake8** - Python linting (manual stage only, see note below)
4. **Trailing whitespace** - Removes trailing spaces
5. **End of files** - Ensures files end with newline
6. **YAML** - Validates YAML syntax
7. **Large files** - Prevents accidental commits of large files
8. **Merge conflicts** - Detects unresolved merge markers
9. **Mixed line endings** - Ensures consistent line endings

**Note:** Flake8 runs only in manual mode (`stages: [manual]`) to provide warnings without blocking commits. This allows developers to see linting issues without disrupting their workflow.

## Setup

Pre-commit hooks are automatically installed when you set up the project:

```bash
# Install pre-commit package (already in requirements.txt)
pip install pre-commit

# Install the git hooks
pre-commit install
```

## Manual Execution

Run checks manually on all files:

```bash
pre-commit run --all-files
```

Run a specific check:

```bash
pre-commit run black
pre-commit run isort
```

## Configuration

Pre-commit configuration is defined in `.pre-commit-config.yaml` at the project root.

### Tool Versions

- **Black**: v24.10.0
- **isort**: v5.13.2 (configured with Black profile)
- **pre-commit-hooks**: v5.0.0

## Bypassing Hooks (Not Recommended)

If absolutely necessary, you can bypass hooks with:

```bash
git commit --no-verify
```

**Warning**: This skips all quality checks and should only be used in emergencies.

## Troubleshooting

### "pre-commit not found"

Ensure you're in the virtual environment:

```bash
# Linux/Mac
source lineup-venv/bin/activate

# Windows
lineup-venv\Scripts\activate
```

### Hooks not running

Reinstall the hooks:

```bash
pre-commit uninstall
pre-commit install
```

### Check failed but code looks correct

Update pre-commit cache:

```bash
pre-commit clean
pre-commit install-hooks
```

## CI/CD Integration

Similar checks run in GitHub Actions as part of the PR validation pipeline:

- **Stage 1: Quick Validation** - Runs Black, isort, Flake8
- **Additional checks:** Trailing whitespace, YAML validation, and other hooks run locally via pre-commit

All checks must pass before PR can be merged.

See `docs/development/ci-cd-pipeline.md` for full CI details.
