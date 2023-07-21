import model
import mongoengine
import copy
import json
import enum
import constants
import helpers

def importData(strings_filename, data_filename, armor_filename):
  # check database for possible existing data

  # load data from files
  strings_file = open(strings_filename)
  data_file = open(data_filename)
  armor_file = open(armor_filename)
  _strings_data = json.load(strings_file)
  strings_data = copy.deepcopy(_strings_data)
  _game_data = json.load(data_file)
  game_data = copy.deepcopy(_strings_data)
  _armor_data = json.load(armor_file)
  armor_data = copy.deepcopy(_armor_data)
  
  # utility functions for getting strings
  def getEntityNameString(entity) -> str:
    return strings_data[str(entity["LanguageNameId"])]
  def getEntityHelpString(entity) -> str:
    return strings_data[str(entity["LanguageHelpId"])]
  
  # insert game data
  # Insert civilizations
  for civName, civInfo in game_data["techtrees"].items():
    civilizationId = game_data["civ_names"][civName]
    civilizationDescription = strings_data[str(game_data["civ_helptexts"][civName])]
    importCivilization(
      name=civName, 
      civilizationId=civilizationId,
      description=civilizationDescription,
      buildings=civInfo["buildings"],
      techs=civInfo["techs"],
      unique=civInfo["unique"],
      units=civInfo["units"]
    )
  # insert armor
  for armorId, armorName in armor_data.items():
    importArmor(armorId=armorId, name=armorName)
  
  # insert buildings
  for buildingId, buildingInfo in game_data["data"]["buildings"]:
    importBuilding(
      entityId=buildingId,
      name=getEntityNameString(buildingInfo),
      helpText=getEntityHelpString(buildingInfo),
      internalName=buildingInfo["internal_name"],
      cost=buildingInfo["Cost"],
      trainTime=buildingInfo["TrainTime"],\
      hp=buildingInfo["HP"],
      meleeArmor=buildingInfo["MeleeArmor"],
      pierceArmor=buildingInfo["PierceArmor"],
      armors=buildingInfo["Armours"],
      attack=buildingInfo["Attack"],
      attacks=buildingInfo["Attacks"],
      reloadTime=buildingInfo["ReloadTime"],
      accuracyPercent=buildingInfo["AccuracyPercent"],
      minRange=buildingInfo["MinRange"],
      range_=buildingInfo["Range"],
      lineOfSight=buildingInfo["LineOfSight"],
      garrisonCapacity=buildingInfo["GarrisonCapacity"],
    )
  # insert techs
  for techId, techInfo in game_data["data"]["techs"]:
    importTech(
      entityId=techId,
      name=getEntityNameString(techInfo),
      helpText=getEntityHelpString(techInfo),
      internalName=techInfo["internal_name"],
      cost=techInfo["Cost"],
      researchTime=techInfo["ResearchTime"],
      repeatable=techInfo["Repeatable"]
    )
  # insert unit upgrades
  for unitUpgradeId, unitUpgradeInfo in game_data["data"]["unit_upgrades"]:
    # The unit upgrade Id is not unique, rather it is the ID of the unit 
    # that this unit upgrades into
    # for example, the long swordsman upgrade has Id = 77
    # and upgrades into the Two Handed Swordsmen. The THS has an ID of 77
    # To get around this, we add the 'ID' field to the JSON ID key, which
    # is always 901 for some reason. Therefore each upgrade will have a 
    # unique ID but also we can maintain the logic/relationship
    # of tech <-> units
    # This can be used in the future to build the line of upgrades for a given unit
    
    importUnitUpgrade(
      entityId=unitUpgradeId + unitUpgradeInfo["ID"],
      name=unitUpgradeInfo["internal_name"],
      researchTime=unitUpgradeInfo["ResearchTime"],
      internalName=unitUpgradeInfo["internal_name"]
    )
  # insert units
  for unitId, unitInfo in game_data["data"]["units"]:
    importUnit(
      entityId=unitId,
      name=getEntityNameString(unitInfo),
      helpText=getEntityHelpString(unitInfo),
      internalName=unitInfo["internal_name"],
      trait=unitInfo["Trait"],
      traitPiece=unitInfo["TraitPiece"],
      cost=unitInfo["Cost"],
      trainTime=unitInfo["TrainTime"],
      hp=unitInfo["HP"],
      meleeArmor=unitInfo["MeleeArmor"],
      pierceArmor=unitInfo["PierceArmor"],
      armors=unitInfo["Armours"],
      attack=unitInfo["Attack"],
      attacks=unitInfo["Attacks"],
      reloadTime=unitInfo["ReloadTime"],
      accuracyPercent=unitInfo["AccuracyPercent"],
      attackDelaySeconds=unitInfo["AttackDelaySeconds"],
      chargeEvent=unitInfo["ChargeEvent"],
      chargeType=unitInfo["ChargeType"],
      maxCharge=unitInfo["MaxCharge"],
      rechargeRate=unitInfo["RechargeRate"],
      frameDelay=unitInfo["FrameDelay"],
      minRange=unitInfo["MinRange"],
      range_=unitInfo["Range"],
      lineOfSight=unitInfo["LineOfSight"],
      garrisonCapacity=unitInfo["GarrisonCapacity"],
      speed=unitInfo["Speed"],
    )
  

  # close files
  strings_file.close()
  data_file.close()
  armor_file.close()

  return

# inserts a single civilization into mongodb
def importCivilization(
  name:str, 
  civilizationId:int, 
  description:str, 
  buildings, 
  techs, 
  unique, 
  units
):
  parsedDescription = helpers.parseCivDescription(description)
  civ = model.Civilization(
    name=name,
    civilizationId=civilizationId,
    description=model.CivilizationDescription(
      civType=parsedDescription["civType"],
      bonuses=parsedDescription["bonuses"],
    ),
    buildings=buildings,
    techs=techs,
    unique=model.UniqueInfo(
      castleAgeUniqueTech=unique["castleAgeUniqueTech"],
      castleAgeUniqueUnit=unique["castleAgeUniqueUnit"],
      imperialAgeUniqueTech=unique["imperialAgeUniqueTech"],
      imperialAgeUniqueUnit=unique["imperialAgeUniqueUnit"],
    ),
    units=units,
  )
  civ.save()

def importUnit(
  entityId:int, 
  name:str, 
  helpText:str, 
  internalName:str, 
  trait:int, 
  traitPiece:int, 
  cost:dict,
  trainTime:float,
  hp:int,
  meleeArmor:int,
  pierceArmor:int,
  armors:dict,
  attack:int,
  attacks:dict,
  reloadTime:float,
  accuracyPercent:int,
  attackDelaySeconds:int,
  chargeEvent:int,
  chargeType:int,
  maxCharge:int,
  rechargeRate:float,
  frameDelay:float,
  minRange:int,
  range_:int,
  lineOfSight:int,
  garrisonCapacity:int,
  speed:float,
):
  type = constants.ENTITY_TYPES["UNIT"]
  unit = model.Entity(
    type = type,
    entityId = entityId,
    name = name,
    helpText = helpers.parseEntityDescription(helpText),
    internalName = internalName,
    trait = trait,
    traitPiece = traitPiece,
    cost = model.Cost(**cost),
    trainTime = trainTime,
    hp = hp,
    meleeArmor = meleeArmor,
    pierceArmor = pierceArmor,
    armors = model.ArmorAttackAmount(**armors),
    attack = attack,
    attacks = model.ArmorAttackAmount(**attacks),
    reloadTime = reloadTime,
    accuracyPercent = accuracyPercent,
    attackDelaySeconds = attackDelaySeconds,
    chargeEvent = chargeEvent,
    chargeType = chargeType,
    maxCharge = maxCharge,
    rechargeRate = rechargeRate,
    frameDelay = frameDelay,
    minRange = minRange,
    range = range_,
    lineOfSight = lineOfSight,
    garrisonCapacity = garrisonCapacity,
    speed = speed,
  )
  unit.save()
  return

def importTech(
  entityId:int, 
  name:str, 
  helpText:str, 
  internalName:str, 
  cost:dict, 
  researchTime:int, 
  repeatable:bool
):
  type = constants.ENTITY_TYPES["TECH"]
  tech = model.Entity(
    type=type,
    entityId=entityId,
    name=name,
    helpText=helpers.parseEntityDescription(helpText),
    internalName=internalName,
    cost=model.Cost(**cost),
    researchTime=researchTime,
    repeatable=repeatable,
  )
  tech.save()
  return

def importUnitUpgrade(
  entityId:int,
  name:str,
  researchTime:int,
  internalName:str,
):
  type = constants.ENTITY_TYPES["UNIT_UPGRADE"]
  unitUpgrade = model.Entity(
    type=type,
    entityId=entityId,
    name=name,
    researchTime=researchTime,
    internalName=internalName,
  )
  unitUpgrade.save()
  return

def importBuilding(
  entityId:int, 
  name:str, 
  helpText:str, 
  internalName:str, 
  cost:dict,
  trainTime:int,
  hp:int,
  meleeArmor:int,
  pierceArmor:int,
  armors:dict,
  attack:int,
  attacks:dict,
  reloadTime:float,
  accuracyPercent:int,
  minRange:int,
  range_:int,
  lineOfSight:int,
  garrisonCapacity:int
):
  type = constants.ENTITY_TYPES["BUILDING"]
  building = model.Entity(
    type=type,
    entityId=entityId,
    name=name,
    helpText=helpers.parseEntityDescription(helpText),
    internalName=internalName,
    cost=model.Cost(**cost),
    trainTime=trainTime,
    hp=hp,
    meleeArmor=meleeArmor,
    pierceArmor=pierceArmor,
    armors=armors,
    attack=attack,
    attacks=model.ArmorAttackAmount(**attacks),
    reloadTime=reloadTime,
    accuracyPercent=accuracyPercent,
    minRange=minRange,
    range=range_,
    lineOfSight=lineOfSight,
    garrisonCapacity=garrisonCapacity,
  )
  building.save()
  
def importArmor(
  armorId:int,
  name:str,
):
  armor = model.Armor(
    armorId=armorId, 
    name=name
  )
  armor.save()