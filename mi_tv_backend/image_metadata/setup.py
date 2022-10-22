from setuptools import setup
import os

# install with: pip install ./image_metadata

datadir = os.path.join('image_metadata','efficientnet_lite0_feature-vector_2')
datafiles = [(d, [os.path.join(d, f) for f in files])
    for d, folders, files in os.walk(datadir)]

setup(
    name='ImageMetadata',
    version='1.0.0',
    packages=['image_metadata'],
    py_modules=["meta_data_creation", "print_metadata"],
    data_files=datafiles,
    description='Writes metadata for images',
    install_requires=[
        "face-recognition",
        "numpy",
        "Pillow",
        "tensorflow",
        "tensorflow-hub",
        "scipy",
        "click",
        "watchdog",
    ],
    entry_points={
        'console_scripts': [
            'meta_data_creation = meta_data_creation:cli',
            'print_metadata = print_metadata:cli',
        ],    
    },
)