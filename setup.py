from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="speechkit",
    version="1.0",
    description="It's lib for using speechkit api by yandex.",
    license="MIT",
    long_description=long_description,
    author="Tikhon Petrishchev",
    author_email="tikhon.petrishchev@gmail.com",
    packages=["speechkit"],
    install_requires=["requests", "io", "json"],
)
