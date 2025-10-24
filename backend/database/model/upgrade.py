from mongoengine import Document, StringField, EnumField, EmbeddedDocumentListField

from backend.constants.data_constants import EntityType
from backend.database.model.model import Cost


class Upgrade(Document):
  id = StringField(required=True, primary_key=True)
  type = EnumField(EntityType, required=True, default_value=EntityType.UPGRADE)
  name = StringField(required=True)
  description = StringField(required=True)
  cost = EmbeddedDocumentListField(Cost, required=True)
