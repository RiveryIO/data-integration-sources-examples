from setuptools import setup, find_packages
import re
from pathlib import Path


init_file = Path(__file__).parent / "data_integration_sources_examples" / "__init__.py"
version = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', init_file.read_text()).group(1)

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="data-integration-sources-examples",
    version=version,
    author="Rivery",
    author_email="dev@rivery.io",
    description="Data integration source example configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={"data_integration_sources_examples": ["examples/**/*"]},
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
