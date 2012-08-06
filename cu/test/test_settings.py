import os.path
import os


class TestFindLocalConfiguration(object):
    @classmethod
    def setup_class(cls):
        from cu.settings import _find_local_configuration
        cls._uut = staticmethod(_find_local_configuration)
        cls._arg_path = os.path.join(os.sep, 'root', 'foo', 'bar',
                                     'cruz', 'blub')
        cls._config_path = os.path.join(os.sep, 'root', 'foo', 'bar',
                                        '.cu.yml')

    def _patch(self, monkeypatch):
        old_impl = os.path.dirname

        def mocked_dirname(path):
            if path == '/root':
                return path
            return old_impl(path)

        def mocked_isfile(path):
            return path == self._config_path

        monkeypatch.setattr(os.path, 'isfile', mocked_isfile)
        monkeypatch.setattr(os.path, 'dirname', mocked_dirname)

    def test_find(self, monkeypatch):
        self._patch(monkeypatch)
        config = self._uut(self._arg_path)
        assert config == self._config_path

    def test_non_existing(self, monkeypatch):
        self._patch(monkeypatch)
        config = self._uut(os.path.join(os.sep, 'root', 'foo'))
        assert config is None


class TestGetLocalSettings(object):
    @classmethod
    def setup_class(cls):
        from cu.settings import get_local_settings
        cls._uut = staticmethod(get_local_settings)

    def test_get_settings(self, monkeypatch, tmpdir):
        p = tmpdir.mkdir('foo')
        p.mkdir('bar')
        p.join('.cu.yml').write("""
                                foo: 22
                                bar: [2, 4, 8]
                                """)
        monkeypatch.setattr(os, 'getcwd',
                            lambda: p.join('bar').dirname)
        config = self._uut()
        assert config['foo'] == 22
        assert len(config['bar']) == 3
