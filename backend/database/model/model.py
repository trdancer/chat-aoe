import mongoengine
import enum

from backend.constants.data_constants import ArmorClass, EntityType, ResourceType

# connection string (should probably be read from a config file) 
# mongodb://127.0.0.1:27017
# TODO create database configuration, validation script


class Cost(mongoengine.EmbeddedDocument):
  value = mongoengine.FloatField(required=True)
  resourceType = mongoengine.EnumField(ResourceType)

class Armor(mongoengine.Document):
  id = mongoengine.EnumField(ArmorClass)
  name = mongoengine.StringField(required=True)
  description = mongoengine.StringField()

class AttackAmount(mongoengine.EmbeddedDocument):
  value = mongoengine.FloatField()
  armorClass = mongoengine.ReferenceField(Armor, required=True)

class ArmorAmount(mongoengine.EmbeddedDocument):
  value = mongoengine.FloatField()
  armorClass = mongoengine.ReferenceField(Armor, required=True)

def createConnection(env, db_version):
  if env == 'PROD' or env == 'PRODUCTION':
    mongoengine.connect(
      db=f'production_chat-aoe_{db_version}',
      host='mongodb://127.0.0.1',
      port=27017
    )
  else:
    mongoengine.connect(
      db=f'development_chat-aoe_{db_version}',
      host='mongodb://127.0.0.1',
      port=27017
    )
# civ = Civilization(
#   name='test', 
#   civilizationId=1, 
#   description='test123', 
#   buildings=[1,2], 
#   techs=[3,4],
#   units = [6, 7]
# )
# civ.save()
# Civilization.objects()