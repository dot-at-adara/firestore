import setuptools, os, sys
version = "1.0"

with open('requirements.txt') as f:
    requirements = f.readlines()
setuptools.setup(
    name='firestore',  # Replace with your own username
    version="0.0.4",
    author="DOT",
    author_email="dot@adara.com",
    description="firestore sub package",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url='https://github.com/dot-at-adara/firestore',
    packages=['framework', 'tests'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=(
        'cookiecutter, Python, projects, project templates, Jinja2, skeleton, scaffolding, '
        'project directory, setup.py, package, packaging'
    ),
    python_requires='>=3.6',
    install_requires=requirements
)
