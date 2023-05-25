import json
import copy
import helpers
from constants import ENTITY_CATEGORIES

# Every tech/unit/civ is unique in the game, so everything can actually be stored in a single mapping
# And looked up by its common name, and we can call the group of units/techs/civs/buildings "entities"

class AOEData():

  game_data = None
  name_info_map = None

  def __init__(self, strings_filename, data_filename):
    # load in the file of strings.json
    # This is the mapping from numbers/keys to descriptions
    strings_file = open(strings_filename)
    data_file = open(data_filename)
    id_description_map = json.load(strings_file)
    self.string_data = copy.deepcopy(id_description_map)
    _game_data_file = json.load(data_file)
    name_info_map = {}
    # This is the mapping from unit/building identifiers to their number/key
    
    new_game_data = copy.deepcopy(_game_data_file)
    
    temp_data = _game_data_file["data"]
    field_names = ["buildings", "units", "techs"]
    for field in field_names:
      for category_id, info in temp_data[field].items():
        nameId = str(info["LanguageNameId"])
        descriptionId = str(info["LanguageHelpId"])
        name = id_description_map[nameId]
        new_game_data["data"][field][name] = info
        appended_entity_info = name_info_map.get(name)
        if appended_entity_info:
          appended_entity_info["info"]["upgrade_info"] = info
          name_info_map[name] = appended_entity_info
        else:
          name_info_map[name] = {
            "id": int(category_id),
            "name": name, 
            "description": helpers.parseEntityDescription(id_description_map[descriptionId]),
            "category": field, 
            "info": info
          }

    for civ_name, id in _game_data_file["civ_helptexts"].items():
      civ_description = id_description_map[id]
      name_info_map[civ_name] = {
        "id": int(id),
        "name": civ_name,
        "description": helpers.parseCivDescription(civ_description),
        "category": ENTITY_CATEGORIES["CIVILIZATION"],
        "uniqueTechnologies": {},
        "info": None,
      }
    
    for id, unit_upgrade_info in temp_data["unit_upgrades"].items():
      unit = _game_data_file["data"]["units"].get(id)
      internal_name = unit_upgrade_info["internal_name"]
      name, description = "", ""
      if not unit:
        # attempt to get the entity by their internal name
        unit = name_info_map.get(internal_name)
        if not unit:
          raise Exception("Unit not found")
        name = unit["name"]
      else:
        
        nameId = unit["LanguageNameId"]
        name = id_description_map[str(nameId)]
        helpId = unit["LanguageHelpId"]
      
      new_game_data["data"]["unit_upgrades"][name] = unit_upgrade_info
      appended_unit_info = name_info_map[name]
      appended_unit_info["info"]["upgrade_info"] = unit_upgrade_info
      name_info_map[name] = appended_unit_info
    for civ, civ_techtree in _game_data_file["techtrees"].items():
      for field in field_names:
        tree_part = civ_techtree[field]
        for id in tree_part:
          # get the common name for the entity ID
          entity_help_id = temp_data[field][str(id)]["LanguageNameId"]
          entity_help_name = id_description_map[str(entity_help_id)]
          # get what civs already have access to this thing
          existing_civs_access = name_info_map[entity_help_name].get("civilizations_access", [])
          existing_civs_access.append(civ)
          name_info_map[entity_help_name]["civilizations_access"] = existing_civs_access
    
    strings_file.close()
    data_file.close()
    self.game_data = new_game_data
    self.info_map = name_info_map
  
  def getEntityInfoByName(self, entity_name:str):
    entity_info = self.info_map.get(helpers.toTitleCase(entity_name))
    if (entity_info == None):
      raise Exception(f'Sorry, I cannot figure out what \"{entity_name}\" is')
    return entity_info
  

  def getEntityCostString(self, entity):
    costs = entity["info"]["Cost"]
    s = f'{entity["name"]} costs:\n'
    for resource, amount in costs.items():
      s += f'\t{amount} {resource}\n'
    maybe_upgrade_info = entity["info"].get("upgrade_info")
    if maybe_upgrade_info:
      upgrade_cost = maybe_upgrade_info["Cost"]
      s += f'\nCost to Research:\n'
      for upgrade_resource, upgrade_amount in upgrade_cost.items():
        s += f'\t{upgrade_amount} {upgrade_resource}\n'
    return s

  def getUnitUpgradeCostString(self, entity):
    maybe_upgrade_info = entity["info"].get("upgrade_info")
    s = f'\nCost to Research/Upgrade to {entity["name"]}:\n'
    if maybe_upgrade_info:
      upgrade_cost = maybe_upgrade_info["Cost"]
      for upgrade_resource, upgrade_amount in upgrade_cost.items():
        s += f'\t{upgrade_amount} {upgrade_resource}\n'
    else:
      s += f'\tNo upgrade needed to get {entity["name"]}'
    return s

  def getUnitInfoString(self, entity):
    info = entity["info"]
    cost = self.getEntityCostString(entity)
    answer = f'{entity["description"]}\n\n' \
            f'{cost}\n\n'                     \
            f'Unit Information\n'                     \
            f'HP:             {info["HP"]}\n' \
            f'Melee Armor:    {info["MeleeArmor"]}\n' \
            f'Pierce Armor:   {info["PierceArmor"]}\n' \
            f'Attack:         {info["Attack"]}\n' \
            f'Range:          {info["Range"]}\n' \
            f'Accuracy:       {info["AccuracyPercent"]}%\n' \
            f'Speed:          {info["Speed"]}\n' \
            f'LOS:            {info["LineOfSight"]}\n' \
            f'Garrison Capac: {info["GarrisonCapacity"]}\n' \
            f'Train Time:     {info["TrainTime"]}\n' \
            f'Reload Time:    {info["ReloadTime"]}\n' \
            f'Attack Delay:   {info["AttackDelaySeconds"]:0.4}\n' \
            f'Frame Delay:    {info["FrameDelay"]}\n' \
            f'Charge Attack:  {info["MaxCharge"]}'
    return answer

  def getBuildingInfoString(self, entity):
    info = entity["info"]
    cost = self.getEntityCostString(entity)
    answer = f'{entity["description"]}\n\n' \
            f'{cost}\n\n'  \
            f'HP:             {info["HP"]}\n' \
            f'Melee Armor:    {info["MeleeArmor"]}\n' \
            f'Pierce Armor:   {info["PierceArmor"]}\n' \
            f'Attack:         {info["Attack"]}\n' \
            f'Range:          {info["Range"]}\n' \
            f'Accuracy:       {info["AccuracyPercent"]}%\n' \
            f'LOS:            {info["LineOfSight"]}\n' \
            f'Garrison Capac: {info["GarrisonCapacity"]}\n' \
            f'Build Time:     {info["TrainTime"]}\n' \
            f'Reload Time:    {info["ReloadTime"]}\n'

    return answer

  def getCivInfoString(self, entity):
    answer = f'{entity["description"]["civ_type"]}\n'
    for bonus in entity["description"]["bonuses"]:
      answer += f'{bonus}\n'
      # entity_match = re.search(entities_string)
    return answer
  
  def getTechInfoString(self, entity):
    answer = f'{self.getEntitityDescriptionString(entity)}\n\n' \
              f'{self.getEntityCostString(entity)}\n'
    return answer

  def getEntitityDescriptionString(self, entity):
    return f'{entity["name"]}\n{entity["description"]}'

  def getEntitityInfoString(self, entity):
    answer = ""
    if (entity["category"] == ENTITY_CATEGORIES["CIVILIZATION"]): 
      answer += self.getCivInfoString(entity)
    elif (entity["category"] == ENTITY_CATEGORIES["BUILDING"]): 
      answer += self.getBuildingInfoString(entity)
    elif (entity["category"] == ENTITY_CATEGORIES["UNIT"]): 
      answer += self.getUnitInfoString(entity)
    elif entity["techs"]:
      answer += self.getTechInfoString(entity)
    return answer

  def getPosessionInfoString(self, _civ_name:str, entity_name:str):
    civ_name = helpers.toTitleCase(_civ_name)
    entity = self.getEntityInfoByName(helpers.toTitleCase(entity_name))
    civ_entity_list = self.game_data["techtrees"][civ_name][entity["category"]]
    entity_id = entity["id"]
    if entity_id in civ_entity_list:
      return f'Yes, {civ_name} do get {entity["name"]}'
    else:
      return f'No, {civ_name} do not get {entity["name"]}'

  def getEntityPossessionString(self, entity_name):
    entity = self.getEntityInfoByName(entity_name)
    civs = entity.get("civilizations_access", None)
    if not civs:
      return 'I\'m sorry I had trouble answering that question'
    if len(civs) == 1:
      return f'Only {civs[0]} get {entity["name"]}'
    
    answer = f'The following civilizations get {entity["name"]}:'
    for c in civs:
      answer += f'\n\t{c}'
    return answer

  def getCivsWithEntity(self, entity_name):
    entity = self.getEntityInfoByName(entity_name)
    
    return entity.get("civilizations_access", None)
  
  def getTechName(self, id):
    tech_info_name_id = self.game_data["data"]["techs"][str(id)]["LanguageNameId"]
    tech_name = self.string_data[str(tech_info_name_id)]
    return tech_name  

  def getCastleAgeTechString(self, civ:str):
    civTitleCase = helpers.toTitleCase(civ)
    uniqueData = self.game_data["techtrees"][civTitleCase]["unique"]
    techId = uniqueData["castleAgeUniqueTech"]
    uniqueTechName = self.getTechName(techId)
    techEntity = self.getEntityInfoByName(uniqueTechName)
    return (uniqueTechName, self.getTechInfoString(techEntity))
  
  def getImperialAgeTechString(self, civ:str):
    civTitleCase = helpers.toTitleCase(civ)
    uniqueData = self.game_data["techtrees"][civTitleCase]["unique"]
    techId = uniqueData["imperialAgeUniqueTech"]
    uniqueTechName = self.getTechName(techId)
    techEntity = self.getEntityInfoByName(uniqueTechName)
    return (uniqueTechName, self.getTechInfoString(techEntity))
  
  def getCivUniqueTechString(self, civ:str, age=None):
    civTitleCase = helpers.toTitleCase(civ)
    title = ''
    answer = ''
    if not age:
      (castleUniqueTechName, castleDescription) = self.getCastleAgeTechString(civ)
      (imperialUniqueTechName, imperialDescription) = self.getImperialAgeTechString(civ)

      title = f'{civTitleCase} unique techs are {castleUniqueTechName} and {imperialUniqueTechName}\n'
      
      answer += f'Castle Age Unique Tech:\n' \
                f'{castleDescription}\n' \
                f'Imperial Age Unique Tech:\n' \
                f'{imperialDescription}'
    elif age.lower() == 'castle':
      (uniqueTechName, description) = self.getCastleAgeTechString(civ)
      title = f'{civTitleCase} Castle Age unique tech is {uniqueTechName}\n'
      answer += description
    
    elif age.lower() == 'imperial':
      (uniqueTechName, description) = self.getImperialAgeTechString(civ)
      title = f'{civTitleCase} Imperial Age unique tech is {uniqueTechName}\n'
      answer += description
    
    return title + answer
  
  def getUnitNameString(self, id):
    nameId = self.game_data["data"]["units"][str(id)]["LanguageNameId"]
    return self.string_data[str(nameId)]
  
  def getCivUniqueUnitString(self, civ):
    civTitleCase = helpers.toTitleCase(civ)
    uniqueData = self.game_data["techtrees"][civTitleCase]["unique"]
    
    castleId = uniqueData["castleAgeUniqueUnit"]
    castleUnitName = self.getUnitNameString(castleId)
    castleEntity = self.getEntityInfoByName(castleUnitName)
    castleUnitDescription = self.getUnitInfoString(castleEntity)
    
    imperialId = uniqueData["imperialAgeUniqueUnit"]
    imperialUnitName = self.getUnitNameString(imperialId)
    imperialEntity = self.getEntityInfoByName(imperialUnitName)
    imperialUnitDescription = self.getUnitInfoString(imperialEntity)

    answer = f'{civTitleCase} Unique Unit from the Castle is {castleUnitName}\n' \
             f'{castleUnitDescription}\n' \
             f'{imperialUnitDescription}'
    
    return answer
