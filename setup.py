import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

reqs = ['torch', "devito"]
setuptools.setup(
    name="conv_scaling",
    version="0.0.5",
    author="Ali Siahkoohi",
    author_email="alisk@gatech.edu",
    description="Small experiments w/ PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alisiahkoohi/conv-scaling",
    license='MIT',
    install_requires=reqs,
    packages=setuptools.find_packages()
)
