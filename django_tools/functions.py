import re

from django.utils.text import slugify as base_slugify


def clear_tr_special_chars(self):
    self = re.sub(r"İ", "i", self)
    self = re.sub(r"I", "i", self)
    self = re.sub(r"Ç", "c", self)
    self = re.sub(r"Ş", "s", self)
    self = re.sub(r"Ü", "u", self)
    self = re.sub(r"Ğ", "g", self)
    self = re.sub(r"Ö", "o", self)
    self = re.sub(r"ö", "o", self)
    self = re.sub(r"ı", "i", self)
    self = re.sub(r"ç", "c", self)
    self = re.sub(r"ş", "s", self)
    self = re.sub(r"ü", "u", self)
    self = re.sub(r"ğ", "g", self)
    return self


def slugify(self):
    self = clear_tr_special_chars(self)
    return base_slugify(self)
