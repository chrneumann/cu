"""
Send letters and e-mails to customers.
"""

import os.path
from subprocess import (
    CalledProcessError,
    check_call,
    check_output,
)
import sys

from docopt import docopt
from mako.template import Template
import mako.exceptions

from cu.customers import load_customers
from cu.settings import get_local_settings


def print_letter(customer, templates, output_path):
    """Print letter.
    """
    pdfs = []
    for template in templates:
        tex = write_letter(customer, template, output_path)
        pdfs.append(compile_latex(tex))
    for pdf in pdfs:
        show_pdf(pdf)


def write_letter(customer, template, output_path):
    """Render letter, write to file and return filename.
    """
    rendered = render_latex_template(template, customer)
    template_name = os.path.splitext(os.path.basename(template))[0]
    out_path = os.path.join(
        output_path,
        customer['filename'] + '_' + template_name + '.tex')
    with open(out_path, 'w') as f:
        f.write(rendered.encode('utf-8'))
    return out_path


def show_pdf(path):  # pragma: no cover
    """Open pdf in user preferred application."""
    check_call(['xdg-open', path])


def compile_latex(path):
    """Compile given latex file and return the resulting PDF's path.
    """
    try:
        check_output([
            'pdflatex', '-halt-on-error',
            '-output-directory=' + os.path.dirname(path),
            path])
    except CalledProcessError, e:
        print sys.stderr, e.output
        raise
    return os.path.join(
        os.path.dirname(path),
        os.path.splitext(os.path.basename(path))[0] + '.pdf')


def render_latex_template(path, context):
    try:
        template = Template(filename=path)
        return template.render_unicode(**context)
    except:
        print mako.exceptions.text_error_template().render()
        raise


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
            templates = []
            for template in settings['mail']['latex_templates']:
                templates.append(os.path.join(
                    basedir, template))
            output_path = os.path.join(
                basedir,
                settings['mail']['output_path'])
            print_letter(customer, templates, output_path)
