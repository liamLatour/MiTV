from setuptools import setup

setup(
    name='ImageMetadata',
    version='0.1.0',
    packages=['image_metadata'],
    scripts=['./bin/meta_data_creation.py'],
    description='Writes metadata for images',
    install_requires=[
        "face-recognition",
        "numpy",
        "Pillow",
        "tensorflow",
        "tensorflow-hub",
        "scipy",
        "click",
    ],
)