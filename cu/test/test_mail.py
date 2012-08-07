from contextlib import nested

from mock import patch


class TestMain(object):
    @classmethod
    def setup_class(cls):
        from cu.mail import main
        cls._uut = staticmethod(main)

    def test_print_letter(self, tmpdir):
        p = tmpdir.mkdir('foo')
        p.mkdir('bar')
        p.mkdir('letters')
        p.join('template.tex').write(
            """
            \\documentclass{article}
            \\begin{document}
            Hey World!
            \\end{document}
            """)
        p.join('.cu.yml').write("""
                                mail:
                                  output_path: letters
                                  latex_template: template.tex
                                """)
        one = p.join('one.yml')
        one.write("""
                  name: Foo
                  """)
        two = p.join('two.yml')
        two.write("""
                  name: Bar
                  """)
        args = [None, 'print-letter', 'one.yml', 'two.yml']
        with nested(
                patch('docopt.sys.argv', args),
                patch('os.getcwd'),
                patch('cu.mail.show_pdf'),
        ) as (argv_mock, cwd_mock, pdf_mock):
            cwd_mock.return_value = p.join('bar').dirname
            self._uut()

        assert pdf_mock.called
        assert p.join('letters', 'one.pdf').check()
        assert p.join('letters', 'two.pdf').check()
