from setuptools import setup, find_packages


setup(
    name="hackernewslib",
    version="0.1.0",
    author="Panagiotis Matigakis",
    author_email="pmatigakis@gmail.com",
    description="Hackernews client library",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "newspaper3k==0.2.8",
        "marshmallow==2.19.2",
        "python-firebase==1.2"
    ],
    setup_requires=[
        "pytest-runner==4.4"
    ],
    tests_require=[
        "pytest==4.4.1"
    ],
    include_package_data=True,
    zip_safe=False
)
