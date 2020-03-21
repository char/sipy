import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sipy",
    version="0.1.0",
    author="half cambodian hacker man",
    author_email="half-kh-hacker@hackery.site",
    description="A lean static site generator in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/half-cambodian-hacker-man/sipy-gen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
      "misaka>=2.1.1",
      "jinja2>=2.11.1"
    ]
)
