from setuptools import setup

# install with: pip install ./image_metadata

setup(
    name='ImageMetadata',
    version='0.5.0',
    packages=['image_metadata'],
    py_modules=["meta_data_creation", "print_metadata"],
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