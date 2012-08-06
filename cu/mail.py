"""
Send letters and e-mails to customers.
"""

from docopt import docopt
import jinja2


latex_jinja_env = dict(
    block_start_string='((*',
    block_end_string='*))',
    variable_start_string='(((',
    variable_end_string=')))',
    comment_start_string='((=',
    comment_end_string='=))',
)


def print_letter(customers):
    pass


def render_latex_template(template, context):
    env = jinja2.Environment(**latex_jinja_env)
    template = env.get_template(template)
    return template.render(**context)


def main():
    __doc__ = """Send letters and e-mails to customers.

    Usage:
      cu-mail print-letter [customers]

    o 'print-letter' generates and prints a letter to the given customers.


    Options:
      -h --help     Show this screen.
    """

    arguments = docopt(__doc__)

    if arguments['print-letter']:
        pass
