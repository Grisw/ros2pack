import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ros2pack",
    version="0.0.1",
    author="Xutao Liu",
    author_email="liuxutao@zju.edu.cn",
    description="Ros 2 Packing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['roslibpy'],
    python_requires='>=3'
)
