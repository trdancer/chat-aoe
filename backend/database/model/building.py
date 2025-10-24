
from mongoengine import Document, StringField, EnumField, GenericReferenceField, EmbeddedDocumentListField, FloatField, BooleanField, ListField, ReferenceField

from backend.constants.data_constants import Age, EntityType
from backend.database.model.effect import Aura
from backend.database.model.model import ArmorAmount, AttackAmount, Cost
from backend.database.model.technology import Technology
from backend.database.model.unit import Unit
from backend.database.model.upgrade import Upgrade


class Building(Document):
  id = StringField(required=True, primary_key=True)
  name = StringField(required=True)
  description = StringField(required=True)
  cost = EmbeddedDocumentListField(Cost, required=True)
  build_time = FloatField()
  hp = FloatField(0)
  attacks = EmbeddedDocumentListField(AttackAmount, default=[])
  armors = EmbeddedDocumentListField(ArmorAmount, default=[])
  min_range = FloatField(0)
  range = FloatField(0)
  line_of_sight = FloatField(0)
  garrison_capacity = FloatField(default=0)
  accuracy = FloatField()
  attack_speed = FloatField()
  reload_time = FloatField()
  frame_delay = FloatField()
  attack_delay = FloatField()
  blast_radius = FloatField()
  conversion_resistance= FloatField()
  convertable = BooleanField()
  regeneration_rate = FloatField()
  healing_rate = FloatField()
  trainable_units = ListField(ReferenceField(Unit))
  technologies = ListField(ReferenceField(Technology))
  upgrades = ListField(ReferenceField(Upgrade))
  population_space_provided = FloatField(default=0)
  population_space_consumed = FloatField(default=0)
  age_available = EnumField(Age)
  upgraded_by = ReferenceField(Upgrade)
  work_rate = FloatField(default=1)
  prev_building = GenericReferenceField()
  next_building = GenericReferenceField()
  auras = EmbeddedDocumentListField(Aura)
