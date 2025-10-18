import os
import sys
import data.model
import mongoengine
import copy
import json
import enum
import constants
import helpers

def importData(strings_filename:str, data_filename:str, armor_filename:str):
  # load data from files
  strings_file = open(strings_filename)
  data_file = open(data_filename)
  armor_file = open(armor_filename)
  _strings_data:dict = json.load(strings_file)
  strings_data = copy.deepcopy(_strings_data)
  _game_data:dict = json.load(data_file)
  game_data = copy.deepcopy(_game_data)
  _armor_data:dict = json.load(armor_file)
  armor_data = copy.deepcopy(_armor_data)
  # utility functions for getting strings
  def getEntityNameString(entity:dict) -> str:
    return strings_data[str(entity["LanguageNameId"])]
  def getEntityHelpString(entity:dict) -> str:
    return strings_data[str(entity["LanguageHelpId"])]
  
  # insert metadata
  patch_version = helpers.parseFileNameVersion(data_filename)
  metadata = data.model.MetaData(patchVersion=patch_version)
  metadata.save()

  # Insert game data
  # Insert civilizations
  print('inserting civilizations...')
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
  print('inserting armors...')
  for armorId, armorName in armor_data.items():
    importArmor(armorId=armorId, name=armorName)
  
  print('inserting buildings...')
  # insert buildings
  count = 0
  for buildingId, buildingInfo in game_data["data"]["buildings"].items():
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
  print(count)
  print('inserting techs...')
  # insert techs
  for techId, techInfo in game_data["data"]["techs"].items():
    importTech(
      entityId=techId,
      name=getEntityNameString(techInfo),
      helpText=getEntityHelpString(techInfo),
      internalName=techInfo["internal_name"],
      cost=techInfo["Cost"],
      researchTime=techInfo["ResearchTime"],
      repeatable=techInfo["Repeatable"]
    )
  print('inserting unit upgrades...')
  # insert unit upgrades
  for unitUpgradeId, unitUpgradeInfo in game_data["data"]["unit_upgrades"].items():
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
      entityId=int(unitUpgradeId) + unitUpgradeInfo["ID"],
      name=unitUpgradeInfo["internal_name"],
      researchTime=unitUpgradeInfo["ResearchTime"],
      internalName=unitUpgradeInfo["internal_name"]
    )
  print('inserting units')
  # insert units
  for unitId, unitInfo in game_data["data"]["units"].items():
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
  civ = data.model.Civilization(
    name=name,
    civilizationId=civilizationId,
    description=data.model.CivilizationDescription(
      civType=parsedDescription["civType"],
      bonuses=parsedDescription["bonuses"],
    ),
    buildings=buildings,
    techs=techs,
    unique=data.model.UniqueInfo(
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
  unit = data.model.Entity(
    type = type,
    entityId = f'{type}_{entityId}',
    name = name,
    helpText = helpers.parseEntityDescription(helpText),
    internalName = internalName,
    trait = trait,
    traitPiece = traitPiece,
    cost = data.model.Cost(**helpers.lowerCaseKeys(cost)),
    trainTime = trainTime,
    hp = hp,
    meleeArmor = meleeArmor,
    pierceArmor = pierceArmor,
    armors=list(map(helpers.makeArmorAttackDict, armors)),
    attack = attack,
    attacks=list(map(helpers.makeArmorAttackDict, attacks)),
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
  tech = data.model.Entity(
    type=type,
    entityId=f'{type}_{entityId}',
    name=name,
    helpText=helpers.parseEntityDescription(helpText),
    internalName=internalName,
    cost=data.model.Cost(**helpers.lowerCaseKeys(cost)),
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
  unitUpgrade = data.model.Entity(
    type=type,
    entityId=f'{type}_{entityId}',
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
  armors:list,
  attack:int,
  attacks:list,
  reloadTime:float,
  accuracyPercent:int,
  minRange:int,
  range_:int,
  lineOfSight:int,
  garrisonCapacity:int
):
  type = constants.ENTITY_TYPES["BUILDING"]
  building = data.model.Entity(
    type=type,
    entityId=f'{type}_{entityId}',
    name=name,
    helpText=helpers.parseEntityDescription(helpText),
    internalName=internalName,
    cost=data.model.Cost(**helpers.lowerCaseKeys(cost)),
    trainTime=trainTime,
    hp=hp,
    meleeArmor=meleeArmor,
    pierceArmor=pierceArmor,
    armors=list(map(helpers.makeArmorAttackDict, armors)),
    attack=attack,
    attacks=list(map(helpers.makeArmorAttackDict, attacks)),
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
  armor = data.model.Armor(
    armorId=armorId, 
    name=name
  )
  armor.save()

def deleteAllGameData():
  # delete armor/attacks
  print('Deleting all Armors...')
  armors = data.model.Armor.drop_collection()
  
  # delete Civilizations
  print('Deleting all Civilizations...')
  civs = data.model.Civilization.drop_collection()

  # delete entities
  print('Deleting all Entities...')
  entities = data.model.Entity.drop_collection()

  # delete metadata
  print('deleting all metadata')
  metadata = data.model.MetaData.drop_collection()

def validateDatabase(data_filename:str, armor_filename:str):
  data_file = open(data_filename)
  armor_file = open(armor_filename)
  _game_data = json.load(data_file)
  game_data = copy.deepcopy(_game_data)
  _armor_data = json.load(armor_file)
  armor_data = copy.deepcopy(_armor_data)
  data_file.close()
  armor_file.close()

  file_patch_version = helpers.parseFileNameVersion(data_filename)
  # print(file_patch_version)
  patch_version_count = data.model.MetaData.objects(patchVersion=file_patch_version).count()
  # print(patch_version_count)
  # number of civs should be equal to the number in the data file
  civ_count = data.model.Civilization.objects().count()
  file_civ_count = len(game_data["techtrees"].keys())
  
  # number of entities should be equal to the sum of the units, techs, upgrades, and buildings
  unit_count = data.model.Entity.objects(type=constants.ENTITY_TYPES["UNIT"]).count()
  file_unit_count = len(game_data["data"]["units"].keys())
  
  unit_upgrade_count = data.model.Entity.objects(type=constants.ENTITY_TYPES["UNIT_UPGRADE"]).count()
  file_unit_upgrade_count = len(game_data["data"]["unit_upgrades"].keys())
  
  tech_count = data.model.Entity.objects(type=constants.ENTITY_TYPES["TECH"]).count()
  file_tech_count = len(game_data["data"]["techs"].keys())
  
  building_count = data.model.Entity.objects(type=constants.ENTITY_TYPES["BUILDING"]).count()
  file_building_count = len(game_data["data"]["buildings"].keys())
  
  # print("# UNIT IN DB", unit_count)
  # print(file_unit_count)
  # print("# UNIT UPGRADE IN DB", unit_upgrade_count)
  # print(file_unit_upgrade_count)
  # print("# TECH IN DB", tech_count)
  # print(file_tech_count)
  # print("# BUILDING IN DB", building_count)
  # print(file_building_count)
  # print("TOTAL IN FILE", file_unit_count + file_unit_upgrade_count + file_tech_count + file_building_count)
  # number of armor classes in database should be equal to the number in the file
  armor_count = data.model.Armor.objects.count()
  file_armor_count = len(armor_data.keys())
  isValid = patch_version_count == 1 and \
            civ_count == file_civ_count and \
            unit_count == file_unit_count and \
            unit_upgrade_count == file_unit_upgrade_count and \
            tech_count == file_tech_count and \
            building_count == file_building_count and \
            armor_count == file_armor_count
  return isValid

def main():
  py_env = os.environ.get('PY_ENV')
  strings_filename = os.environ.get('STRINGS_FILE')
  data_filename = os.environ.get('DATA_FILE')
  armor_filename = os.environ.get('ARMOR_FILE')
  validate_only = os.environ.get('VALIDATE_ONLY')
  if (not py_env):
    py_env = 'DEV'
  if (not strings_filename):
    print('STRINGS_FILE environment variable required.')
    sys.exit(1)
  if (not data_filename):
    print('DATA_FILE environment variable required.')
    sys.exit(1)
  if (not armor_filename):
    print('ARMOR_FILE environment variable required.')
    sys.exit(1)
  
  patch_version = helpers.parseFileNameVersion(data_filename)
  data.model.createConnection(py_env, patch_version)

  # check database for possible existing data
  isValid = validateDatabase(data_filename, armor_filename)
  if (not isValid and not validate_only):
    print('database invalid, reimporting all game data')
    deleteAllGameData()
    importData(strings_filename, data_filename, armor_filename)
    print('Database is valid, exiting.')
  if (validate_only):
    print('Database status:', 'VALID' if isValid else 'INVALID')
  mongoengine.disconnect()
  sys.exit(0)

if __name__ == "__main__":
  main()