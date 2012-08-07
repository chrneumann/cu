import os.path


class TestLoadCustomers(object):
    @classmethod
    def setup_class(cls):
        from cu.customers import load_customers
        cls._uut = staticmethod(load_customers)

    def test_load(self, monkeypatch, tmpdir):
        p = tmpdir.mkdir('foo')
        petes = p.join('petes_flasks.yml')
        petes.write(
            """
            name: "Pete's Flasks"
            """)
        up = p.join('up.yml')
        up.write(
            """
            name: "United Profit"
            """)
        customers = self._uut(
            os.path.join(p.dirname, p.basename),
            [os.path.join(petes.dirname, petes.basename),
             os.path.join(up.dirname, up.basename)])
        assert len(customers) == 2
        assert customers[0]['name'] == "Pete's Flasks"
        assert customers[0]['filename'] == "petes_flasks"
        assert customers[1]['name'] == "United Profit"
        assert customers[1]['filename'] == "up"
