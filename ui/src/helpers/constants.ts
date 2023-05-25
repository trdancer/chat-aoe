import dayJs from 'dayjs'

export const DATE_FORMAT = 'hh:mma MM/DD/YYYY'

export const formatTimestamp = (t:number) => {
  return dayJs.unix(t).format(DATE_FORMAT)
}

export const apiUrl = 'http://localhost:5000/api/v1/'

export const QUESTION_TYPES = {
  "COST": 0,
  "POSSESSION": 1,
  "INFO": 2,
  "UNIQUE_TECH": 3,
  "UNIQUE_UNIT": 4,
  "ENTITY_POSSESSION": 5,
}

export const CIVILIZATIONS = new Set([
  "Aztecs",
  "Bengalis",
  "Berbers",
  "Bohemians",
  "Britons",
  "Bulgarians",
  "Burgundians",
  "Burmese",
  "Byzantines",
  "Celts",
  "Chinese",
  "Cumans",
  "Dravidians",
  "Ethiopians",
  "Franks",
  "Goths",
  "Gurjaras",
  "Hindustanis",
  "Huns",
  "Incas",
  "Italians",
  "Japanese",
  "Khmer",
  "Koreans",
  "Lithuanians",
  "Magyars",
  "Malay",
  "Malians",
  "Mayans",
  "Mongols",
  "Persians",
  "Poles",
  "Portuguese",
  "Saracens",
  "Sicilians",
  "Slavs",
  "Spanish",
  "Tatars",
  "Teutons",
  "Turks",
  "Vietnamese",
  "Vikings",
])