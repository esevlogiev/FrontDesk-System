import re

LOCAL_FORMAT = r'\b0([1-9]|[ ()-]{1,2}\d)([ ()-]{,2}\d){5,10}\b'
INTERNATIONAL_FORMAT = r'((00|\+)[1-9]\d{0,2})([ ()-]{,2}\d){6,11}\b'
POSITIVE_FLOAT_NUMBER = r'^(0|[1-9][0-9]*)(\.[0-9]+)?$'
POSITIVE_INTEGER = r'^(0|[1-9][0-9]*)$'
PERSON_NAME = r'^[A-Z][a-z]*$'
ITEM_NAME = r'^[a-z][a-z]*$'
NAME = r'^[A-Za-z][A-Za-z]*$'


class Validations:
    @classmethod
    def equal(cls, pattern, value):
        match = re.search(pattern, value)
        if not match:
            return False
        start, end = match.span()
        if value[start:end] == value:
            return True
        return False

    @classmethod
    def is_phone(cls, value):
        return (Validations.equal(INTERNATIONAL_FORMAT, value) or
                Validations.equal(LOCAL_FORMAT, value))

    @classmethod
    def is_float_number(cls, value):
        return Validations.equal(POSITIVE_FLOAT_NUMBER, value)

    @classmethod
    def is_positive_integer(cls, value):
        return Validations.equal(POSITIVE_INTEGER, value)

    @classmethod
    def is_person_name(cls, value):
        return Validations.equal(PERSON_NAME, value)

    @classmethod
    def is_item_name(cls, value):
        return Validations.equal(ITEM_NAME, value)

    @classmethod
    def is_name(cls, value):
        return Validations.equal(NAME, value)
