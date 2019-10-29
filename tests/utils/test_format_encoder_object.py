import unittest
from datetime import datetime

from bson import ObjectId

from app.utils.format_encoder_object import format_encoder_object


class TestFormatEncoderObject(unittest.TestCase):
    def test_type_objectid(self):
        formated = format_encoder_object(ObjectId())
        self.assertIsInstance(formated, str)

    def test_type_date(self):
        formated = format_encoder_object(datetime.now())
        self.assertIsInstance(formated, str)

    def test_type_str(self):
        formated = format_encoder_object("sdfsdf")
        self.assertIsInstance(formated, str)

    def test_type_not_str(self):
        formated = format_encoder_object("sdfsdf")
        self.assertNotIsInstance(formated, int)


if __name__ == "__main__":
    unittest.main()
