import mongoengine
import enum
# connection string (should probably be read from a config file) 
# mongodb://127.0.0.1:27017
# TODO create database initilization, validation script
mongoengine.connect(
  db='chat-aoe',
  host='mongodb://127.0.0.1',
  port=27017
)

class EntityType(enum.Enum):
  BULDING = "BUILDING"
  UNIT = "UNIT"
  UNIT_UPGRADE = "UNIT_UPGRADE"
  TECHNOLOGY = "TECHNOLOGY"


class Cost(mongoengine.EmbeddedDocument):
  wood = mongoengine.IntField()
  food = mongoengine.IntField()
  gold = mongoengine.IntField()
  stone = mongoengine.IntField()

class Armor(mongoengine.Document):
  armorId = mongoengine.IntField(required=True, primary_key=True)
  name = mongoengine.StringField(required=True)

class ArmorAttackAmount(mongoengine.EmbeddedDocument):
  armorId = mongoengine.ReferenceField(Armor, required=True, primary_key=True)
  amount = mongoengine.IntField(required=True)

class Entity(mongoengine.Document):
    # Meta
    type = mongoengine.EnumField(EntityType, required=True)
    entityId = mongoengine.IntField(required=True, primary_key=True)
    name = mongoengine.StringField(required=True)
    helpText = mongoengine.StringField()
    internalName = mongoengine.StringField(required=True)
    # Unit only meta
    trait: mongoengine.IntField()
    traitPiece: mongoengine.IntField()

    # Creation
    cost = mongoengine.EmbeddedDocumentField(Cost)
    trainTime = mongoengine.FloatField()
    
    # Armor
    hp = mongoengine.IntField()
    meleeArmor = mongoengine.IntField()
    pierceArmor = mongoengine.IntField()
    armors = mongoengine.EmbeddedDocumentListField(ArmorAttackAmount)
    
    # Attack
    attack = mongoengine.IntField()
    attacks = mongoengine.EmbeddedDocumentListField(ArmorAttackAmount)
    reloadTime = mongoengine.FloatField()
    accuracyPercent = mongoengine.IntField()
    # Units only Attack
    attackDelaySeconds = mongoengine.FloatField()
    chargeEvent = mongoengine.IntField()
    chargeType = mongoengine.IntField()
    maxCharge = mongoengine.IntField()
    rechargeRate = mongoengine.FloatField()
    frameDelay = mongoengine.FloatField()

    # Distance
    minRange = mongoengine.IntField()
    range = mongoengine.IntField()
    lineOfSight = mongoengine.IntField()

    # Size
    garrisonCapacity = mongoengine.IntField()

    # Unit only Speed
    speed = mongoengine.FloatField()

    # Unit Upgrades and techs only
    researchTime = mongoengine.IntField()
    
    # Techs only:
    repeatable = mongoengine.BooleanField(default=False)

class UniqueInfo(mongoengine.EmbeddedDocument):
  castleAgeUniqueTech = mongoengine.IntField()
  castleAgeUniqueUnit = mongoengine.IntField()
  imperialAgeUniqueTech = mongoengine.IntField()
  imperialAgeUniqueUnit = mongoengine.IntField()

class CivilizationDescription(mongoengine.EmbeddedDocument):
  civType = mongoengine.StringField()
  bonuses = mongoengine.ListField(mongoengine.StringField())
  
class Civilization(mongoengine.Document):
  name = mongoengine.StringField(unique=True, required=True)
  civilizationId = mongoengine.IntField(primary_key=True, required=True)
  description = mongoengine.EmbeddedDocumentField(CivilizationDescription, required=True)
  buildings = mongoengine.ListField(mongoengine.IntField())
  techs = mongoengine.ListField(mongoengine.IntField())
  unique = mongoengine.EmbeddedDocumentField(UniqueInfo)
  units = mongoengine.ListField(mongoengine.IntField())

civ = Civilization(
  name='test', 
  civilizationId=1, 
  description='test123', 
  buildings=[1,2], 
  techs=[3,4],
  units = [6, 7]
)
civ.save()
Civilization.objects()