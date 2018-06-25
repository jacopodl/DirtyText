from setuptools import setup, find_packages

setup(
    name="dirtytext",
    version="1.0.0",
    description="Searches for [ab]using of Unicode glyphs",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jacopodl/dirtytext",
    author="Jacopo De Luca",
    author_email="jacopo.delu@gmail.com",
    license="GNU General Public License v3",
    keywords=["dirty", "text", "tool", "unicode", "UTF-8", "glyph"],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3"
    ], entry_points={
        'console_scripts': ['dirtytext=dirtytext.__main__:main']
    })
