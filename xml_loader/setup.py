from setuptools import setup, find_packages

setup(
    name="xml_loader",
    version="0.1",
    packages=find_packages(),
    install_requires=['core>=0.1'],
    entry_points={
        'prodavnica.ucitati':
            ['xml_loader=xml_loader.xml_loader:XmlLoader'],
    },
    zip_safe=False
)