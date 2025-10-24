from enum import Enum
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, EnumField, StringField, ReferenceField, ListField
from backend.constants.data_constants import ArchitectureType
from backend.database.model.building import Building
from backend.database.model.effect import EffectInAge
from backend.database.model.technology import Technology
from backend.database.model.unit import Unit
from backend.database.model.upgrade import Upgrade


class BonusType(Enum):
    Civilization = 0
    Team = 1

class Bonus(EmbeddedDocument):
    effects = ListField(ReferenceField(EffectInAge))
    bonusType = EnumField(BonusType)
    description = StringField()

class Civilization(Document):
    name = StringField()
    type = StringField()
    bonuses = EmbeddedDocumentListField(Bonus)
    unique_units = ListField(ReferenceField(Unit))
    unique_buildings = ListField(ReferenceField(Building))
    unique_technologies = ListField(ReferenceField(Technology))
    unique_upgrades = ListField(ReferenceField(Upgrade))

    technologies = ListField(ReferenceField(Technology))
    upgrades = ListField(ReferenceField(Upgrade))
    buildings = ListField(ReferenceField(Building))
    units = ListField(ReferenceField(Unit))

    architecture = EnumField(ArchitectureType)