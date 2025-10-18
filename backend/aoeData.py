import json
import copy
import helpers
from constants import ENTITY_CATEGORIES

# Every tech/unit/civ is unique in the game, so everything can actually be stored in a single mapping
# And looked up by its common name, and we can call the group of units/techs/civs/buildings "entities"

class AOEData():

  game_data = None
  name_info_map = None

  def __init__(self, strings_filename, data_filename, armor_filename):
    # load in the file of strings.json
    # This is the mapping from numbers/keys to descriptions
    strings_file = open(strings_filename)
    data_file = open(data_filename)
    armor_file = open(armor_filename)
    id_description_map = json.load(strings_file)
    self.string_data = copy.deepcopy(id_description_map)
    _game_data_file = json.load(data_file)
    name_info_map = {}
    # This is the mapping from unit/building identifiers to their number/key
    
    armor_data = json.load(armor_file)
    self.armor_data = copy.deepcopy(armor_data)
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
    armor_file.close()
    self.game_data = new_game_data
    self.info_map = name_info_map
  
  def getEntityInfoByName(self, entity_name:str):
    entity_info = self.info_map.get(helpers.toTitleCase(entity_name))
    if (entity_info == None):
      raise Exception(f'Sorry, I cannot figure out what \"{entity_name}\" is')
    return entity_info
  
  def getEntityAttackString(self, entity):
    info = entity["info"]
    answer = f'<div class="entity-bonus-damage">Bonus Damage:<ul>'
    for attack_info in info["Attacks"]:
      attack_class = attack_info["Class"]
      attack_amount = attack_info["Amount"]
      entity_class_string = self.armor_data[str(attack_class)]
      answer += f'<li class="entity-bonus-damage-item"><b>{entity_class_string}</b>: {attack_amount}</li>'
    answer += f'</ul></div>'
    return answer
  
  def getEntityArmorString(self, entity):
    info = entity["info"]
    answer = f'<div class="entity-armor-class">Armor Classes:<ul>'
    for armor_info in info["Armours"]:
      armor_class = armor_info["Class"]
      armor_amount = armor_info["Amount"]
      entity_class_string = self.armor_data[str(armor_class)]
      answer += f'<li class="entity-armor-class-item"><b>{entity_class_string}</b>: {armor_amount}</li>'
    answer += f'</ul></div>'
    return answer
  
  def getEntityCostString(self, entity):
    costs = entity["info"]["Cost"]
    s = f'<div class="entity-cost">{entity["name"]} costs:<ul>'
    for resource, amount in costs.items():
      s += f'<li class="entity-cost-item">{amount} {resource}</li>'
    s += f'</ul>'
    maybe_upgrade_info = entity["info"].get("upgrade_info")
    if maybe_upgrade_info:
      upgrade_cost = maybe_upgrade_info["Cost"]
      s += f'<div class="entity-upgrade-cost">Cost to Research:<ul>'
      for upgrade_resource, upgrade_amount in upgrade_cost.items():
        s += f'<li class="entity-upgrade-cost-item">{upgrade_amount} {upgrade_resource}</li>'
      s += f'</ul>'
    s += f'</div>'
    return s

  def getUnitUpgradeCostString(self, entity):
    maybe_upgrade_info = entity["info"].get("upgrade_info")
    if maybe_upgrade_info:
      s = f'<div class="unit-upgrade-cost">Cost to Research/Upgrade to {entity["name"]}:<ul>'
      upgrade_cost = maybe_upgrade_info["Cost"]
      for upgrade_resource, upgrade_amount in upgrade_cost.items():
        s += f'<li class="unit-upgrade-cost-item">{upgrade_amount} {upgrade_resource}</li>'
      s += f'</ul></div>'
    else:
      return f'No upgrade needed to get {entity["name"]}'
    return s

  def getUnitInfoString(self, entity):
    info = entity["info"]
    cost = self.getEntityCostString(entity)
    answer = f'<span class="entity-name">{entity["name"]}</span><br>' \
            f'<span class="entity-description">{entity["description"]}</span>' \
            f'{cost}'                     \
            f'<span class="entity-information">Unit Information</span>'                     \
            f'<ul>' \
            f'<li class="entity-information-item"><b>HP:</b>             {info["HP"]}</li>' \
            f'<li class="entity-information-item"><b>Melee Armor:</b>    {info["MeleeArmor"]}</li>' \
            f'<li class="entity-information-item"><b>Pierce Armor:</b>   {info["PierceArmor"]}</li>' \
            f'<li class="entity-information-item"><b>Attack:</b>         {info["Attack"]}</li>' \
            f'<li class="entity-information-item"><b>Range:</b>          {info["Range"]}</li>' \
            f'<li class="entity-information-item"><b>Accuracy:</b>       {info["AccuracyPercent"]}%</li>' \
            f'<li class="entity-information-item"><b>Speed:</b>          {info["Speed"]}</li>' \
            f'<li class="entity-information-item"><b>LOS:</b>            {info["LineOfSight"]}</li>' \
            f'<li class="entity-information-item"><b>Garrison Capac:</b> {info["GarrisonCapacity"]}</li>' \
            f'<li class="entity-information-item"><b>Train Time:</b>     {info["TrainTime"]}</li>' \
            f'<li class="entity-information-item"><b>Reload Time:</b>    {info["ReloadTime"]}</li>' \
            f'<li class="entity-information-item"><b>Attack Delay:</b>   {info["AttackDelaySeconds"]:0.4}</li>' \
            f'<li class="entity-information-item"><b>Frame Delay:</b>    {info["FrameDelay"]}</li>' \
            f'<li class="entity-information-item"><b>Charge Attack:</b>  {info["MaxCharge"]}</li>' \
            f'</ul>'
    answer += self.getEntityAttackString(entity)
    answer += self.getEntityArmorString(entity)
    return answer

  def getBuildingInfoString(self, entity):
    info = entity["info"]
    cost = self.getEntityCostString(entity)
    answer = f'<span class="entity-name">{entity["name"]}</span><br>' \
            f'<span class="entity-name">{entity["description"]}</span>' \
            f'{cost}'  \
            f'<span class="entity-information">Building Information</span>'                     \
            f'<ul>' \
            f'<li class="entity-information-item"><b>HP:</b>             {info["HP"]}</li>' \
            f'<li class="entity-information-item"><b>Melee Armor:</b>    {info["MeleeArmor"]}</li>' \
            f'<li class="entity-information-item"><b>Pierce Armor:</b>   {info["PierceArmor"]}</li>' \
            f'<li class="entity-information-item"><b>Attack:</b>         {info["Attack"]}</li>' \
            f'<li class="entity-information-item"><b>Range:</b>          {info["Range"]}</li>' \
            f'<li class="entity-information-item"><b>Accuracy:</b>       {info["AccuracyPercent"]}%</li>' \
            f'<li class="entity-information-item"><b>LOS:</b>            {info["LineOfSight"]}</li>' \
            f'<li class="entity-information-item"><b>Garrison Capac:</b> {info["GarrisonCapacity"]}</li>' \
            f'<li class="entity-information-item"><b>Build Time:</b>     {info["TrainTime"]}</li>' \
            f'<li class="entity-information-item"><b>Reload Time:</b>    {info["ReloadTime"]}</li>' \
            f'</ul>'
    answer += self.getEntityAttackString(entity)
    answer += self.getEntityArmorString(entity)
    return answer

  def getCivInfoString(self, entity):
    answer = f'<span class="civ-type">{entity["description"]["civType"]}</span><ul class="civ-bonuses">'
    for bonus in entity["description"]["bonuses"]:
      answer += f'<li class="civ-bonus-item">{bonus}</li>'
      # entity_match = re.search(entities_string)
    answer += f'</ul>'
    return answer
  
  def getTechInfoString(self, entity):
    answer = f'{self.getEntityDescriptionString(entity)}<br>' \
              f'{self.getEntityCostString(entity)}'
    return answer

  def getEntityDescriptionString(self, entity):
    return f'<span class="entity-name">{entity["name"]}</span><br>{entity["description"]}'

  def getEntitityInfoString(self, entity):
    answer = ""
    if (entity["category"] == ENTITY_CATEGORIES["CIVILIZATION"]): 
      answer += self.getCivInfoString(entity)
    elif (entity["category"] == ENTITY_CATEGORIES["BUILDING"]): 
      answer += self.getBuildingInfoString(entity)
    elif (entity["category"] == ENTITY_CATEGORIES["UNIT"]): 
      answer += self.getUnitInfoString(entity)
    elif (entity["category"] == ENTITY_CATEGORIES["TECH"]):
      answer += self.getTechInfoString(entity)
    return answer

  def getPosessionInfoString(self, _civ_name:str, entity_name:str):
    civ_name = helpers.toTitleCase(_civ_name)
    entity = self.getEntityInfoByName(helpers.toTitleCase(entity_name))
    civ_entity_list = self.game_data["techtrees"][civ_name][entity["category"]]
    entity_id = entity["id"]
    if entity_id in civ_entity_list:
      return f'Yes, <span class="civ-name">{civ_name}</span> do get <span class="entity-name">{entity["name"]}</span>'
    else:
      return f'No, <span class="civ-name">{civ_name}</span> do not get <span class="entity-name">{entity["name"]}</span>'

  def getEntityPossessionString(self, entity_name):
    entity = self.getEntityInfoByName(entity_name)
    civs = entity.get("civilizations_access", None)
    if not civs:
      return 'I\'m sorry I had trouble answering that question'
    if len(civs) == 1:
      return f'Only <span class="civ-name">{civs[0]}</span> get  <span class="entity-name">{entity["name"]}</span>'
    
    answer = f'The following civilizations get  <span class="entity-name">{entity["name"]}</span>:<ul>'
    for civ in civs:
      answer += f'<li class="civ-name civ-access-item">{civ}</li>'
    answer += f'</ul>'
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

      title = f'<span class="civ-name">{civTitleCase}</span> unique techs are' \
              f'<span class="entity-name">{castleUniqueTechName}</span> and <span class="entity-name">{imperialUniqueTechName}</span><br>'
      
      answer += f'<span class="unique-tech-header"><span class="entity-name">{castleUniqueTechName}</span> (Castle Age):</span><br>' \
                f'{castleDescription}<br>' \
                f'<span class="unique-tech-header"><span class="entity-name">{imperialUniqueTechName}</span> (Imperial Age):</span><br>' \
                f'{imperialDescription}'
    elif age.lower() == 'castle':
      (uniqueTechName, description) = self.getCastleAgeTechString(civ)
      title = f'<span class="civ-name">{civTitleCase}</span> Castle Age unique tech is <span class="entity-name">{uniqueTechName}</span><br>'
      answer += description
    
    elif age.lower() == 'imperial':
      (uniqueTechName, description) = self.getImperialAgeTechString(civ)
      title = f'<span class="civ-name">{civTitleCase}</span> Imperial Age unique tech is <span class="entity-name">{uniqueTechName}</span><br>'
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

    answer = f'<span class="civ-name">{civTitleCase}</span> Unique Unit from the Castle is the <span class="entity-name">{castleUnitName}</span><br>' \
             f'{castleUnitDescription}<br>' \
             f'{imperialUnitDescription}'
    
    return answer
  
  def getRelatedEntities(self, entities):
    newEntities = []
    for e in entities:
      try:
        full_entity = self.getEntityInfoByName(e)
        small_entity = {
          "name": full_entity["name"],
          "category": full_entity["category"],
        }
        newEntities.append(small_entity)
      except:
        continue
    return newEntities