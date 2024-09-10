from setuptools import setup, find_packages

setup(
    name="simple-visualizer",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["visualizer_simple"],
    entry_points={
        'visualizer':
            ['visualizer_simple=visualizer_simple.visualizer_simple:SimpleVisualizer'],
    },
    zip_safe=True
)
