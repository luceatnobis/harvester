#!/usr/bin/env python3

import pdb
import unittest

from os.path import join

from harvester.plugins.imgur import Imgur


class ImgurTestSingle(unittest.TestCase):

    def setUp(self):
        self.test_dict = [{
            'collection': None,
            'content_id': 'e1yYXUU',
            'content_url': 'https://i.imgur.com/e1yYXUU.jpg',
            'content_hash': 'c2002691d4cd350aca016a982983ce0a',
        }]

    def test_fetch_imgur_share(self):
        msg = "https://imgur.com/e1yYXUU"

        klass = Imgur(msg)
        klass.get_content()
        for i, m in enumerate(klass):
            d = self.test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_fetch_imgur_image_no_i(self):
        msg = "https://imgur.com/e1yYXUU.jpg"
        klass = Imgur(msg)
        klass.get_content()
        for i, m in enumerate(klass):
            d = self.test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_fetch_imgur_raw_image(self):
        msg = "https://i.imgur.com/e1yYXUU.jpg"
        klass = Imgur(msg)
        klass.get_content()
        for i, m in enumerate(klass):
            d = self.test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_path_single(self):
        msg = "https://imgur.com/e1yYXUU"
        klass = Imgur(msg)
        self.assertEquals(klass.return_path(), 'imgur')
        

class ImgurTestComma(unittest.TestCase):

    def test_fetch_imgur_share_comma(self):
        test_dict = [{
            'collection': None,
            'content_id': 'yK2C3KZ',
            'content_url': 'https://i.imgur.com/yK2C3KZ.png',
            'content_hash': 'b1867f10a1c3fb93b3280515b202d0ac',
        }, {
            'collection': None,
            'content_id': 'qn3HVUT',
            'content_url': 'https://i.imgur.com/qn3HVUT.jpg',
            'content_hash': '859be87b32d4eefdcbef391bb63faee5',
        }, {
            'collection': None,
            'content_id': 'GfbYRhJ',
            'content_url': 'https://i.imgur.com/GfbYRhJ.png',
            'content_hash': '5b2463266f958a5041cde08c594a040f',
        }]

        msg = "https://imgur.com/yK2C3KZ,qn3HVUT,GfbYRhJ"

        klass = Imgur(msg)
        klass.get_content()

        self.assertEquals(klass.items, 3)
        for i, m in enumerate(klass):
            d = test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_path_comma(self):
        msg = "https://imgur.com/yK2C3KZ,qn3HVUT,GfbYRhJ"
        klass = Imgur(msg)
        self.assertEquals(klass.return_path(), 'imgur')


class ImgurTestA(unittest.TestCase):

    def setUp(self):
        self.test_dict = [{
            'site': 'imgur',
            'collection': 'Tkx0P',
            'content_id': 'HMk3d7r',
            'content_url': 'https://i.imgur.com/HMk3d7r.png',
            'content_hash': '037c2962e627cdfd347528445e383cd7',
        }, {
            'site': 'imgur',
            'collection': 'Tkx0P',
            'content_id': 'Mq3eWP5',
            'content_url': 'https://i.imgur.com/Mq3eWP5.png',
            'content_hash': '98a6b2f27d27d712ff430ac980cbfb48',
        }, {
            'site': 'imgur',
            'collection': 'Tkx0P',
            'content_id': 'WK8jjDp',
            'content_url': 'https://i.imgur.com/WK8jjDp.png',
            'content_hash': '8a4a37f78a1a3e593a61ab231ce93ed7',
        }, {
            'site': 'imgur',
            'collection': 'Tkx0P',
            'content_id': 'HFXxTMp',
            'content_url': 'https://i.imgur.com/HFXxTMp.png',
            'content_hash': 'c63ff1c939582db2023dd7bc49fd76be',
        }, {
        }]

    def test_fetch_imgur_a(self):
        msg = "https://imgur.com/a/Tkx0P"

        klass = Imgur(msg)
        klass.get_content()
        self.assertEquals(4, klass.items)
        for i, m in enumerate(klass):
            d = self.test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_fetch_imgur_a_contaminated(self):
        msg = "https://imgur.com/a/Tkx0P,"

        klass = Imgur(msg)
        klass.get_content()
        self.assertEquals(4, klass.items)
        for i, m in enumerate(klass):
            d = self.test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_path_a(self):
        msg = "https://imgur.com/a/Tkx0P"
        klass = Imgur(msg)
        self.assertEquals(
            klass.return_path(), join('imgur', 'a', 'Tkx0P'))


class ImgurTestGallery(unittest.TestCase):
    def setUp(self):

        self.test_dict = [{
            'collection': 'P7u9z',
            'content_id': 'aFDjukM',
            'content_url': 'https://i.imgur.com/aFDjukM.png',
            'content_hash': 'b7caefeae792415b4570e5d0b6b633ea',
        }, {
            'collection': 'P7u9z',
            'content_id': 'GDnuadf',
            'content_url': 'https://i.imgur.com/GDnuadf.png',
            'content_hash': 'e52bf7e50b68ecbdb2d34ec0f2bae9b2',
        }, {
            'collection': 'P7u9z',
            'content_id': 'EUEJqpi',
            'content_url': 'https://i.imgur.com/EUEJqpi.png',
            'content_hash': '14f7a5f391340444bfca381bcbfe0391',
        }, {
            'collection': 'P7u9z',
            'content_id': 'tksJuZE',
            'content_url': 'https://i.imgur.com/tksJuZE.png',
            'content_hash': '940c32679c4b8d0f9144283dde90611e',
        }, {
        }]

    def test_fetch_imgur_gallery(self):
        msg = "https://imgur.com/gallery/P7u9z"

        klass = Imgur(msg)
        klass.get_content()
        self.assertEquals(4, klass.items)
        for i, m in enumerate(klass):
            d = self.test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_fetch_imgur_gallery_contaminated(self):
        msg = "https://imgur.com/gallery/P7u9z,"

        klass = Imgur(msg)
        klass.get_content()
        self.assertEquals(4, klass.items)
        for i, m in enumerate(klass):
            d = self.test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_fetch_imgur_long_gallery(self):
        msg = "https://imgur.com/gallery/UhcNd"
        hashes = """
            e58202b6c1a3000de448e9022e766bf1 abbcf77857ce7e6e288a8aff67f535ea
            343fa7e7b62489cfd9d3845f7daeafbb b63c717b9c8b486f1e192f6eea249fd3
            88b23795e2ca3f0f7d485dbe61e2c8e8 878e8fb6c5dd589f44769840d6e1a85d
            8dfdad27cbc48ce3d67ae52385ff5360 6805640833893333add7ba1acdb123be
            f0dd983f5a44feb25a25855fa2e667df 238b0c756083976f79ebd6634ce4703e
            d690b6b45cfe9d9172b61d2cb3517bcd 4345c8d4f870e0aae4195a9fe87f8b58
            076724965bac08b12f081c6bc15fc324 495a53950e5b890088c363858876ed15
            4ecf57341e3047a07c93d0d0524c4077 8fa180b344cd66ae4d114145b8aef169
            d55b4f384743de6913e451ff2dbec441 77d154631d6efeb2c2b24d21f4194a5c
            4e7b854d878badb8609db5c001406679 99d70c523efd5c0bfec30bd93abe3d38
            974a7160efdb403556744541a2656848 26366b4964a5afa6156976f047206077
            67ba0d9efdba1af1134d425f1fca7d75 7bc729b0951db2770375c0dad2a2ae43
            2095049391c315e0f0c37a84ef2b7bee 19fa39ee3246d5ba58ec776ffb108467
            111c6570439fe1d715deae0141e07bc4 d56817bcfd7ab0eea28decad1e0448b5
            4a7f7e3062ff7ea7d297ce341d125c75 8aff169eb7d7e90cc9574aea45c7281c
            72271e9c4fc46428ded96c12f5198db4 56f1f1a4e5df5dc12caedfd290d7c9bc
            4657f7c7854452c76dc0db89b2182c4b c62b8b0cd1ca175674d9545b7aae5138
            1967401a9eac695d2cab1e602cbcf1dd 58d0f1787cd55bac2e62c922f9f62537
            fb03fb4dd2ba7f142ed50843689035a6 396e0b1be787a12bc839645cf861b102
            0dfc77882959a5fd9f689214a933901d 0d8c54abdab168983b24195a231e9b7e
            4672c3bed94330a7d11fb1d2665d5a96 cabf0f3587b09b284411394790c66536
            fe75c24be8e044632095fa0946e3bb9f ce68ed7e518fb91e15d8caa3f7b8c995
            ea5aa7c5064acecd195b13ed3afed7b0 2a61b6572191b20c553f9eb3323286e6
            6948b10efc3053fb983882d78be26486 029a93ae4409fb8edbdb2e9273ceade7
            10e2d2c257e1d35fa4f83f738080fc98 d7238d43def6ba4bfd9fce353b138fde
            b10ee737a6509277a44ca82d0351f750 e6f831cd7603ca9b71f83ed5703c7d20
            e35f0c3d24cd1b3adace994347b2bd0a 458f8e9fe82a6ed9d57d3e5f0180e136
            eb8d53c6460992346d4e473a88abe741 cf744429322f510c2f8c01ac80098fa9
            047db3a40ea3c4803174103fd37d8a98 cfd665edc2b908772ff3e32e80bb3a81
        """
        hashes = [x.strip().split(" ") for x in hashes.split("\n") if x]
        hashes = [x for x in sum(hashes, []) if x]

        klass = Imgur(msg)
        klass.get_content()

        self.assertEquals(58, klass.items)
        for i, m in enumerate(klass):
            [self.assertEquals(hashes[i], m['content_hash'])]

    def test_fetch_imgur_gallery_single_entry(self):  # yes that happens
        test_dict = [{
            'collection': '3kMJEDV',
            'content_id': '3kMJEDV',
            'content_url': 'https://i.imgur.com/3kMJEDV.jpg',
            'content_hash': '0334557ddbb9d909a3e31bd9070e90f7',
        }]

        msg = "https://imgur.com/gallery/3kMJEDV"

        klass = Imgur(msg)
        klass.get_content()
        self.assertEquals(1, klass.items)
        for i, m in enumerate(klass):
            d = test_dict[i]
            [self.assertEquals(v, m[k]) for k, v in d.items()]

    def test_path_gallery(self):
        msg = "https://imgur.com/gallery/3kMJEDV"
        klass = Imgur(msg)
        self.assertEquals(
            klass.return_path(), join('imgur', 'gallery', '3kMJEDV'))

if __name__ == '__main__':
    unittest.main()
