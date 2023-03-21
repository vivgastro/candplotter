from setuptools import setup

requirements = ['numpy', 'matplotlib', 'pandas']

setup(
        version='1.0.0',
        description='Candidates plotter',
        author='Vivek Gupta',
        author_email='vivek.gupta@csiro.au',
        python_requires='>=3.6',
        packages=['candplotter'],
        entry_points = {'console_scripts': ['plot_cands=candplotter.craco_candviewer:main']}
        )

