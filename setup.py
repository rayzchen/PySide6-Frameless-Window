import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="PySide6-Frameless-Window",
    version="0.0.11",
    keywords="pyside6 frameless",
    author="Ray Chen",
    author_email="tankimarshal2@gmail.com",
    description="Based off PyQt5-Frameless-Window but migrated to PySide6.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/rayzchen/PySide6-Frameless-Window",
    packages=setuptools.find_packages(),
    install_requires=[
        "PySide6",
        "pywin32; platform_system == 'Windows'",
        "xcffib; platform_system != 'Windows'",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
