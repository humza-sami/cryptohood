from setuptools import setup, find_packages

setup(
    name="cryptohood",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests>=2.25.0", "pandas>=2.0.0", "python-dotenv>=0.19.0"],
    author="Humza Sami",
    author_email="humzasami20@gmail.com",
    description="A Python wrapper for the Robinhood Crypto API that simplifies cryptocurrency trading and market data access",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/humza-sami/cryptohood",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
