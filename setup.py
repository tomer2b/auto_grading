from setuptools import setup, find_packages

setup(
    name="auto_grading",
    version="0.306",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    package_data={
        'auto_grading': ['tasks.csv'],  # Specify the path relative to the package

    },    
    description="A module for automatic grading python assignments for students",
    author="Tomer Tubi",
    author_email="tomer2b@gmail.com",
    url="https://github.com/tomer2b/auto_grading",
    license="GPL-3.0-or-later",  # Specify GPL version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
