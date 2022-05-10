from setuptools import setup

setup(
    name="serializer-lab",
    packages=[
        "modules",
        "modules/serializers",
        "data",
        "config"
    ],
    version="1.0.0",
    author="Tinkldeath",
    description='console serializer',
    scripts=["main.py"]
)