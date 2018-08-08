import os
import sys

def main():
    REPO_DIR = os.path.dirname(os.path.abspath(__file__))
    DOCS_DIR = os.path.join(REPO_DIR, 'docs')
    DOCS_SRC = os.path.join(DOCS_DIR, 'sources')
    FIGS_DIR = os.path.join(DOCS_DIR, 'figures')

    os.system('python -m aebm.validation.generate {}'.format(FIGS_DIR))
    os.system('sphinx-build -b html {} {}'.format(DOCS_SRC, DOCS_DIR))

if __name__ == '__main__':
    main()
