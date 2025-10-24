from enum import Enum
from mongoengine import EnumField, FloatField, EmbeddedDocument, Document, StringField, ReferenceField, BooleanField, ListField

from backend.constants.data_constants import Age
from backend.database.model.building import Building
from backend.database.model.technology import Technology
from backend.database.model.unit import Unit
from backend.database.model.upgrade import Upgrade

class EffectAttribute(Enum):
    HP = 0
    Accuracy = 1
    AttackRate = 2
    Range = 3
    MinRange = 4
    BlastRadius = 5
    MovementSpeed = 6
    WorkRate = 7
    ConversionResistance = 8
    HealRate = 9
    RegenerationRate = 10
    CostAll = 11
    CostFood = 12
    CostWood = 13
    CostStone = 14
    CostGold = 15
    AgeAvailable = 16
    CreationTime = 17
    PopulationConsumed = 18
    PopulationSpaceProvided = 19
    GatherCapacityAll = 20
    # GatherCapacity...
    GatherRateAll = 21
    # GatherRate...
    # AuraRange
    # AuraEffect
    WonderAttack = 22
    InfantryAttack = 23
    HeavyWarshipAttack = 24
    BaseMeleeAttack = 25
    BasePierceAttack = 26
    WarElephantAttack = 27
    CavalryAttack = 28
    AllBuildingAttack = 29
    StoneDefenseAttack = 30
    PredatorAnimalAttack = 31
    ArcherAttack = 32
    NonFishingShipAttack = 33
    HighPierceSiegeAttack = 34
    TreeAttack = 35
    UniqueUnitAttack = 36
    SiegeUnitAttack = 37
    StandardBuildingAttack = 38
    WallAndGateAttack = 39
    GunpowderAttack = 40
    HuntedPredatorAnimalAttack = 41
    MonkAttack = 42
    CastleAttack = 43
    SpearmenAttack = 44
    MountedArcherAttack = 45
    ShockInfantryAttack = 46
    CamelAttack = 47
    UnblockableMeleeAttack = 48
    CondottieroAttack = 49
    UnusedAttack = 50
    FishingShipAttack = 51
    MamelukeAttack = 52
    HeroesAndKingsAttack = 53
    HeavySiegeAttack = 54
    SkirmisherAttack = 55
    RoyalHeirsAttack = 56
    HouseAttack = 57

    WonderArmor = 58
    InfantryArmor = 59
    HeavyWarshipArmor = 60
    BaseMeleeArmor = 61
    BasePierceArmor = 62
    WarElephantArmor = 63
    CavalryArmor = 64
    AllBuildingArmor = 65
    StoneDefenseArmor = 66
    PredatorAnimalArmor = 67
    ArcherArmor = 68
    NonFishingShipArmor = 69
    HighPierceSiegeArmor = 70
    TreeArmor = 71
    UniqueUnitArmor = 72
    SiegeUnitArmor = 73
    StandardBuildingArmor = 74
    WallAndGateArmor = 75
    Gunpowderrmork = 76
    HuntedPredatorAnimalArmor = 77
    MonkArmor = 78
    CastleArmor = 79
    SpearmenArmor = 80
    MountedArcherArmor = 81
    ShockInfantryArmor = 82
    CamelArmor = 83
    UnblockableMeleeArmor = 84
    CondottieroArmor = 85
    UnusedArmor = 86
    FishingShipArmor = 87
    MamelukeArmor = 88
    HeroesAndKingsArmor = 89
    HeavySiegeArmor = 90
    SkirmisherArmor = 91
    RoyalHeirsArmor = 92
    HouseArmor = 93

class EffectType(Enum):
    Add = 1
    Subtract = 2
    Multiply = 3
    Set = 4

class Effect(Document):
    id = StringField(primary_key=True, required=True)
    effected_buildings = ListField(ReferenceField(Building))
    effects_all_buildings = BooleanField(default=False)
    effected_upgrades = ListField(ReferenceField(Upgrade))
    effects_all_upgrades = BooleanField(default=False)
    effected_technologies = ListField(ReferenceField(Technology))
    effects_all_technologies = BooleanField(default=False)
    effected_units = ListField(ReferenceField(Unit))
    effects_ull_units = BooleanField(default=False)
    effect_type = EnumField(EffectType)
    attribute_effected = EnumField(EffectAttribute)
    effect_value = FloatField()


class EffectInAge(EmbeddedDocument):
    effect = ReferenceField(Effect)
    age_applicable = EnumField(Age)

class Aura(EmbeddedDocument):
    effect = ReferenceField(Effect)
    range = FloatField()