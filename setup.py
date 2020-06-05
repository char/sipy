import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sipy",
    version="0.3.1",
    author="half cambodian hacker man",
    author_email="half-kh-hacker@hackery.site",
    description="A lean static site generator in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/half-cambodian-hacker-man/sipy",
    packages=["sipy", "sipy.ext"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
      "misaka>=2.1.1",
      "jinja2>=2.11.1",
      "PyYAML>=5.3.1",
      "watchdog>=0.10.2"
    ],
    entry_points={
      "console_scripts": [
        'sipy = sipy.__main__:main'
      ]
    }
)
