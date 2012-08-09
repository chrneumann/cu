from contextlib import nested
import os.path

from mock import (
    patch,
    call,
)


def test_compile_latex(tmpdir):
    from cu.mail import compile_latex
    tex = tmpdir.join('template.tex')
    tex.write(
        u"""
        \\documentclass{article}
        \\begin{document}
        \xe4
        \\end{document}
        """.encode('utf-8'), 'wb')
    pdf = compile_latex(os.path.join(tex.dirname, tex.basename))
    assert os.path.isfile(pdf)
    assert pdf == os.path.join(
        tex.dirname,
        os.path.splitext(tex.basename)[0] + '.pdf')


class TestMain(object):
    @classmethod
    def setup_class(cls):
        from cu.mail import main
        cls._uut = staticmethod(main)

    def _create_env(self, p):
        p.join('.cu.yml').write(
            u"""
            foo: \xe4
            mail:
              smtp:
                host: localhost
                port: 123
                username: pete
                password: flasks4all
              output_path: letters
              email_template: mail.yml.mako
              latex_templates: [template.tex,
                template2.tex]
            """.encode('utf-8'), 'wb')
        one = p.join('one.yml')
        one.write("""
                  name: Foo
                  email: foo@example.com
                  contacts:
                    -
                      forename: John
                      surename: Doe
                  """)
        two = p.join('two.yml')
        two.write("""
                  name: Bar
                  email: bar@example.com
                  contacts:
                    -
                      forename: Jane
                      surename: Smith
                  """)

    def test_print_letter(self, tmpdir):
        p = tmpdir.mkdir('foo')
        p.mkdir('bar')
        p.mkdir('letters')
        p.join('template.tex').write(
            u"""## -*- coding: utf-8 -*-
            \\documentclass{article}
            \\begin{document}
            Hey ${'World'}!
            \xe4
            \\end{document}
            """.encode('utf-8'), 'wb')
        p.join('template2.tex').write(
            u"""
            \\documentclass{article}
            \\begin{document}
            More World!
            \\end{document}
            """.encode('utf-8'), 'wb')
        self._create_env(p)
        args = [None, 'print-letter', 'one.yml', 'two.yml']
        with nested(
                patch('docopt.sys.argv', args),
                patch('os.getcwd'),
                patch('cu.mail.show_pdf'),
        ) as (argv_mock, cwd_mock, pdf_mock):
            cwd_mock.return_value = p.join('bar').dirname
            self._uut()

        assert pdf_mock.called
        assert p.join('letters', 'one_template.pdf').check()
        assert p.join('letters', 'one_template2.pdf').check()
        assert p.join('letters', 'two_template.pdf').check()
        assert p.join('letters', 'two_template2.pdf').check()

    def test_send_mail(self, tmpdir):
        template = tmpdir.join('mail.yml.mako')
        template.write(
            u"""## -*- coding: utf-8 -*-
            from: '"Pete" <hello@flasks.com>'
            to: '"${contacts[0]['forename']}
              ${contacts[0]['surename']}" <${email}>'
            subject: Buy one, pay for three!
            body: |
              Dear ${contacts[0]['surename']},

              you are great!\xe4
            """.encode('utf-8'), 'wb')
        self._create_env(tmpdir)
        args = [None, 'send-email', 'one.yml', 'two.yml']
        with nested(
            patch('docopt.sys.argv', args),
            patch('os.getcwd'),
            patch('smtplib.SMTP_SSL'),
        ) as (argv_mock, cwd_mock, smtp_mock):
            cwd_mock.return_value = os.path.join(
                tmpdir.dirname, tmpdir.basename)
            self._uut()

        smtp_mock.assert_called_with('localhost', 123)
        smtp_mock.return_value.login.assert_called_with('pete', 'flasks4all')
        sendmail = smtp_mock.return_value.sendmail

        sender = '"Pete" <hello@flasks.com>'
        assert sendmail.call_args_list[0][0][0] == sender
        assert sendmail.call_args_list[0][0][1]\
            == '"John Doe" <foo@example.com>'
        assert "Buy one, pay for three!"\
            in sendmail.call_args_list[0][0][2]
        assert "Dear Doe,\n\nyou are great!"\
            in sendmail.call_args_list[0][0][2]
        assert "=C3=A4" in sendmail.call_args_list[0][0][2]

        assert sendmail.call_args_list[1][0][0] == sender
        assert sendmail.call_args_list[1][0][1]\
            == '"Jane Smith" <bar@example.com>'
        assert "Buy one, pay for three!"\
            in sendmail.call_args_list[1][0][2]
        assert "Dear Smith,\n\nyou are great!"\
            in sendmail.call_args_list[1][0][2]
        assert "=C3=A4" in sendmail.call_args_list[1][0][2]
