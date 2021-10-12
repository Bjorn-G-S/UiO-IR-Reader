from setuptools import setup, find_packages

setup(name='uio_irreader',
      version='0.1.1',
      description='A python packge to convert IR Opus files',
      url='https://github.uio.no/SMN-Catalysis/UiO-IR-Reader',
      license='MIT',
      entry_points={
        'console_scripts': [
            'uio_irreader=uio_irreader.bin.uio_irreader:main',
        ]
      },
      include_package_data=True,
      packages=find_packages(),
      install_requires=['numpy>=1.19.1', 'pandas>=1.2.3', 'argparse>=1.4.0',
                        'matplotlib>=3.3.1', 'brukeropusreader==1.3.4'],
      python_requires='>=3.8.8'
    )
