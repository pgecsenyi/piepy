import sys
from pylint.lint import Run

def main():

    arguments = [
        '--rcfile=.pylintrc',
        'app',
        'bll',
        'dal',
        'indexing',
        'multimedia',
        'testing',
        'web',
        'main',
        'lint_runner',
        'test_runner',
    ]

    if '-e' in sys.argv:
        arguments.append('--errors-only')

    error_code = Run(arguments)
    sys.exit(error_code)

if __name__ == '__main__':

    main()
