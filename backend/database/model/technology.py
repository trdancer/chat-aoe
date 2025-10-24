

from mongoengine import Document, ListField, ReferenceField, GenericReferenceField, StringField, FloatField, EmbeddedDocumentListField, EnumField

from backend.constants.data_constants import Age, EntityType
from backend.database.model.building import Building
from backend.database.model.effect import Effect
from backend.database.model.model import Cost


class Technology(Document):
  id = StringField(required=True, primary_key=True)
  name = StringField(required=True)
  description = StringField(required=True)
  cost = EmbeddedDocumentListField(Cost, required=True)
  effects = ListField(ReferenceField(Effect))
  research_time = FloatField()
  building_researched_from = ReferenceField(Building)
  age_available = EnumField(Age)
  prev_technology = GenericReferenceField()
  next_technology = GenericReferenceField()
  required_technologies = ListField(GenericReferenceField())
  