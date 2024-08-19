from setuptools import setup, find_packages

setup(
    name="pydnacode",
    version="0.1.0",
    description="A Python module for DNA code construction and analysis using coding theory.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Muhammad Arsyad",  
    author_email="muharsyad2201@gmail.com",  
    url="https://github.com/muharsyad/pydnacode",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12.5",
    install_requires=[
        # Tambahkan dependensi jika ada, misalnya:
        # 'numpy>=1.19',
    ],
)
