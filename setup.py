import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="Parser",
    version="1.0",
    author="yezz123",
    author_email="yasserth19@protonmail.com",
    description="Pure python standard library JSON.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="Python , Json , Parser",
    url="https://github.com/Py-Project/Parser",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License (MIT)",
        "Topic :: Lab :: Library",
        "Operating System :: OS Independent"
    ),
)