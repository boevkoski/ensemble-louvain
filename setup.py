from distutils.core import setup
setup(
  name = 'ensemble-louvain',         # How you named your package folder (MyLib)
  packages = ['ensemble-louvain'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Ensemble wrapper of Louvain for stable and accurate communities',   # Give a short description about your library
  author = 'Bojan Evkoski',                   # Type in your name
  author_email = 'bojan.evkoski@ijs.si',      # Type in your E-Mail
  url = 'https://github.com/boevkoski/ensemble-louvain',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Communities', 'Clustering', 'Networks'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'networkx',
          'python-louvain',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Researchers, Developers',      # Define that your audience are developers
    'Topic :: Community Detection',
    'License :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)