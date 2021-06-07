import pytest
from bson.decimal128 import Decimal128

from mongoengine import *
from tests.utils import MongoDBTestCase


class Decimal128Document(Document):
    dec128_fld = Decimal128Field()
    dec128_min_0 = Decimal128Field(min_value=0)
    dec128_max_100 = Decimal128Field(max_value=100)


def generate_test_cls() -> Document:
    Decimal128Document.drop_collection()
    Decimal128Document(dec128_fld=None).save()
    Decimal128Document(dec128_fld=Decimal128("1")).save()
    return Decimal128Document


class TestDecimal128Field(MongoDBTestCase):
    def test_decimal128_validation_good(self):
        """Ensure that invalid values cannot be assigned."""

        doc = Decimal128Document()

        doc.dec128_fld = Decimal128("0")
        doc.validate()

        doc.dec128_fld = Decimal128("50")
        doc.validate()

        doc.dec128_fld = Decimal128("110")
        doc.validate()

    def test_decimal128_validation_invalid(self):
        """Ensure that invalid values cannot be assigned."""

        doc = Decimal128Document()

        doc.dec128_fld = "ten"

        with pytest.raises(ValidationError):
            doc.validate()

    def test_decimal128_validation_min(self):
        """Ensure that out of bounds values cannot be assigned."""

        doc = Decimal128Document()

        doc.dec128_min_0 = Decimal128("50")
        doc.validate()

        doc.dec128_min_0 = Decimal128("-1")
        with pytest.raises(ValidationError):
            doc.validate()

    def test_decimal128_validation_max(self):
        """Ensure that out of bounds values cannot be assigned."""

        doc = Decimal128Document()

        doc.dec128_max_100 = Decimal128("50")
        doc.validate()

        doc.dec128_max_100 = Decimal128("101")
        with pytest.raises(ValidationError):
            doc.validate()

    def test_eq_operator(self):
        cls = generate_test_cls()
        assert 1 == cls.objects(dec128_fld=1.0).count()
        assert 0 == cls.objects(dec128_fld=2.0).count()

    def test_ne_operator(self):
        cls = generate_test_cls()
        assert 1 == cls.objects(dec128_fld__ne=None).count()
        assert 1 == cls.objects(dec128_fld__ne=1).count()
        assert 1 == cls.objects(dec128_fld__ne=1.0).count()

    def test_gt_operator(self):
        cls = generate_test_cls()
        assert 1 == cls.objects(dec128_fld__gt=0.5).count()

    def test_lt_operator(self):
        cls = generate_test_cls()
        assert 1 == cls.objects(dec128_fld__lt=1.5).count()
