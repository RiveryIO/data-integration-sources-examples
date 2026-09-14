# Data Integration Sources Examples

Python library of example JSON configurations for data integration sources. Provides reusable GET/POST request examples for each source-to-target combination.

## Installation

### From JFrog (Recommended)
```bash
pip install data-integration-sources-examples
```

### From Source (Development)
```bash
git clone git@bitbucket.org:boomii/data-integration-sources-examples.git
cd data-integration-sources-examples
pip install -e .
```

## Structure

All examples live **inside the package**, under
`data_integration_sources_examples/examples/`, keyed **first by integration type**, then
source, report, and target — a fixed four-level tree:

```
data_integration_sources_examples/examples/
└── {integration_type}/     # custom_report | predefined
    └── {source}/           # connector name (e.g. jira, adobe_analytics, shopify)
        └── {report}/       # see per-type note below
            └── {target}/   # target system (e.g. snowflake, s3, knowledge_hub)
                ├── get.json     # full API response shape (GET)
                └── post.json    # request body for create/update (POST)
```

> **Why the package prefix matters:** setuptools only packages data *under* the Python
> package directory. Examples at the repo root are not shipped in the wheel — which is why
> they must live under `data_integration_sources_examples/examples/`.

The `{report}` segment differs by integration type:

- **`custom_report/{source}/{report}/{target}/`** — `{report}` is the specific report /
  object name (e.g. `sprint`, `users`, `insight_report`). One river = one report.
- **`predefined/{source}/all_predefined_reports/{target}/`** — the synthetic segment
  `all_predefined_reports` is always used: a single predefined river ingests **all** of the
  source's predefined reports in one flow (`run_type=predefined_report`).

A source can appear under **both** `custom_report/` and `predefined/` (e.g. `jira`,
`facebook_ads`, `intercom`) — they are simply two independent subtrees keyed by the top-level
integration type.

**Example paths:**
```
data_integration_sources_examples/examples/custom_report/jira/sprint/knowledge_hub/get.json
data_integration_sources_examples/examples/custom_report/adobe_analytics/users/snowflake/get.json
data_integration_sources_examples/examples/predefined/jira/all_predefined_reports/snowflake/get.json
data_integration_sources_examples/examples/predefined/shopify/all_predefined_reports/s3/get.json
```

## Adding Examples

```bash
# Custom report (pick one report):
mkdir -p data_integration_sources_examples/examples/custom_report/{source}/{report}/{target}

# Predefined report (always `all_predefined_reports`; one dir per target):
mkdir -p data_integration_sources_examples/examples/predefined/{source}/all_predefined_reports/{target}
```

Then drop `get.json` + `post.json` in the leaf dir and bump the version (see Contributing).

## Helper Functions

Paths passed to `load_example` are **relative to the examples root**
(`{integration_type}/{source}/{report}/{target}/...`) — do not include the
`data_integration_sources_examples/examples/` prefix.

```python
from data_integration_sources_examples import helpers

# Discover what's available
helpers.list_integration_types()                       # ['custom_report', 'predefined']
helpers.list_sources('custom_report')                  # ['jira', 'adobe_analytics', ...]
helpers.list_reports('custom_report', 'jira')          # ['sprint', 'project', ...]
helpers.list_targets('custom_report', 'jira', 'sprint')  # ['knowledge_hub', ...]

# Load a custom report example
data = helpers.load_example('custom_report/jira/sprint/knowledge_hub/post.json')

# Load a predefined report example (covers all reports for this source × target)
data = helpers.load_example('predefined/shopify/all_predefined_reports/snowflake/get.json')
```

## Verification

```bash
python3 verify_library.py
```

## Contributing

### Version Bumping (Required)

Before creating a PR, bump the version in `data_integration_sources_examples/__init__.py`:

```python
__version__ = "0.1.1"  # Increment this
```

The CI/CD pipeline blocks PRs that don't include a version bump.

### Development Workflow

1. Create a feature branch from `main`
2. Add or update example JSON files
3. Bump version in `__init__.py`
4. Create PR — Harness CI/CD runs tests automatically
5. After approval, merge to `main` — package publishes to JFrog

### Running Tests Locally

```bash
pip install -e ".[test]"
pytest
```
