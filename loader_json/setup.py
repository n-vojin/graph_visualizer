from setuptools import setup, find_packages

setup(
    name="json-loader",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["loader_json"],
    entry_points={
        'loader':
            ['loader_json=loader_json.JSONloader:JSONLoader'],
    },
    zip_safe=True
)
