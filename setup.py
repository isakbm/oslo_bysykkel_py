from setuptools import setup

setup(
    name='oslo_bysykkel',
    author='isakbm',
    version='0.0.0',
    description='Just a cute little wrapper around a gbfs endpoint',
    packages=['oslo_bysykkel'],
    package_dir={
        'oslo_bysykkel': '.'
    },
    url='https://github.com/isakbm/oslo_bysykkel_py',
    license='OPEN',
    install_requires=[
        'requests',
    ]
)