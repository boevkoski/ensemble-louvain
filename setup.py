from distutils.core import setup

setup(
    name='elouvain',
    packages=['elouvain'],
    version='0.1',
    license='MIT',
    description='Ensemble wrapper of Louvain for stable and accurate communities',
    author='Bojan Evkoski',
    author_email='bojan.evkoski@ijs.si',
    url='https://github.com/boevkoski/ensemble-louvain',
    download_url='https://github.com/boevkoski/ensemble-louvain/archive/refs/tags/v_01.zip',
    keywords=['Communities', 'Clustering', 'Networks'],
    install_requires=[
        'networkx',
        'python-louvain',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Researchers, Developers',  # Define that your audience are developers
        'Topic :: Community Detection',
        'License :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
