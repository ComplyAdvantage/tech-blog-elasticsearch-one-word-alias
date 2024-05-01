from enum import Enum

from mimesis import Person
from mimesis import Field, Fieldset, Schema
from mimesis.enums import TimestampFormat

from es import INDEX

ENTITY_COUNT = 100000
person = Person()

class EntityType(Enum):
    PERSON = 'person'
    ORGANISATION = 'organisation'

class AmlType(Enum):
    SANCTION = 'sanction'
    WARNING = 'warning'
    PEP = 'pep'

    @classmethod
    def values(cls):
        return tuple(aml_type.value for aml_type in cls)

def alias(random, **kwargs):
    name = person.full_name().lower()
    if random.random() > 0.8:
        return {
            "name": name.split()[0],
            "is_weak": False,
            "word_count": 1,
            "aml_type": AmlType.SANCTION.value,
        }
    return {
        "name": name,
        "is_weak": random.choices((False, True), (0.95, 0.05))[0],
        "word_count": len(name.split()),
        "aml_type": random.choices(AmlType.values(), (0.3, 0.4, 0.3))[0],
    }

field = Field(seed=0xff)
fieldset = Fieldset(seed=0xff)
fieldset.register_handler("alias", alias)

schema_definition = lambda: {
    "_index": INDEX,
    "_id": field("increment"),
    "_source": {
        "created_at": field("timestamp", fmt=TimestampFormat.POSIX),
        "primary_name": field("person.full_name", key=str.lower),
        "birthdate": field("person.birthdate"),
        "type": EntityType.PERSON.value,
        "aliases": fieldset("alias", i=3),
        "country_code": field("address.country_code"),
        "addresses": fieldset("address.address", i=2)
    }
}

entity_builder = Schema(schema=schema_definition, iterations=ENTITY_COUNT)
