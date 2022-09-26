from setuptools import find_packages, setup

setup(
    name="matchmaker",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flask", "requests", "gunicorn"],
)
