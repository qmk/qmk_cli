"""Useful helper functions.
"""
from milc import cli


def question(question, boolean=True, default=''):
    """Asks the user to answer a question.

    This keeps re-asking until it gets acceptible input.
    """
    if cli.args.yes:
        return True

    if default and default.lower() == 'y':
        answer_key = 'Y/n'
    elif default and default.lower() == 'n':
        answer_key = 'y/N'
    else:
        answer_key = 'y/n'

    prompt = '*** %s [%s] ' % (question, answer_key)

    while True:
        answer = input(prompt)
        if answer == '' and default.lower() == 'y':
            answer = 'y'
        elif answer == '' and default.lower() == 'n':
            answer = 'n'

        if answer.lower() in ['y', 'yes']:
            return True
        elif answer.lower() in ['n', 'no']:
            return False
        else:
            cli.args.echo('Invalid answer!')
