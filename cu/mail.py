"""
Send letters and e-mails to customers.
"""

import os.path
from subprocess import (
    check_call,
    check_output,
)
import sys

from docopt import docopt
import jinja2

from cu.customers import load_customers
from cu.settings import get_local_settings


latex_jinja_env = dict(
    block_start_string='((*',
    block_end_string='*))',
    variable_start_string='(((',
    variable_end_string=')))',
    comment_start_string='((=',
    comment_end_string='=))',
)


def print_letter(customer, template, output_path):
    """Print letter.
    """
    tex = write_letter(customer, template, output_path)
    pdf = compile_latex(tex)
    show_pdf(pdf)


def write_letter(customer, template, output_path):
    """Render letter, write to file and return filename.
    """
    rendered = render_latex_template(template, customer)
    out_path = os.path.join(
        output_path,
        customer['filename'] + '.tex')
    with open(out_path, 'w') as f:
        f.write(rendered)
    return out_path


def show_pdf(path):  # pragma: no cover
    """Open pdf in user preferred application."""
    check_call(['xdg-open', path])


def compile_latex(path):
    """Compile given latex file."""
    check_output([
        'pdflatex',
        '-output-directory=' + os.path.dirname(path),
        path])


def render_latex_template(template, context):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.dirname(template)
        ),
        **latex_jinja_env
    )
    template = env.get_template(os.path.basename(template))
    return template.render(**context)


def main():
    __doc__ = """Send letters and e-mails to customers.

    Usage:
      cu-mail print-letter [<customer>...]

    o 'print-letter' generates and prints a letter to the given customers.


    Options:
      -h --help     Show this screen.
    """

    arguments = docopt(__doc__, sys.argv[1:])
    (path, settings) = get_local_settings()
    basedir = os.path.dirname(path)
    customers = load_customers(basedir, arguments['<customer>'])

    if arguments['print-letter']:
        for customer in customers:
            template = os.path.join(
                basedir,
                settings['mail']['latex_template'])
            output_path = os.path.join(
                basedir,
                settings['mail']['output_path'])
            print_letter(customer, template, output_path)
