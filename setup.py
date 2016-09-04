from setuptools import setup, find_packages


setup(name='cloudapp',
      version='0.0.0.dev',
      description="Command-line tool for CloudApp",
      long_description='',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
      ],
      keywords='',
      url='https://github.com/storborg/cloudapp',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      # Don't require six newer than this, el capitan will hate you.
      install_requires=[
          'six>=1.4.1',
          'requests',
      ],
      license='MIT',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False,
      entry_points="""\
      [console_scripts]
      cloudapp = cloudapp:main
      """)
