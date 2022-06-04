import config
from dataclasses import dataclass

@dataclass
class Language:
    lang_key: str
    channel_id: int
    footer: str
    breaking: str

languages: [Language] = [
  Language(
    "en", # English
    config.CHANNEL_EN, # https://t.me/MilitaryNewsEN
    "🔰 Subscribe to @MilitaryNewsEN\n🔰 Join us @MilitaryChatEN",
    "BREAKING_NEWS"),
  
  Language(
    "tr", # Turkish
     -1001712502236, # https://t.me/MilitaryNewsTR
     "🔰@MilitaryNewsTR'e abone olun\n🔰Bize katılın @MNChatTR",
    "SON_DAKİKA"
  ),

  Language(
    "fa", # Persian
    -1001568841775, # https://t.me/MilitaryNewsFA
    "\nعضو شوید:\n🔰 @MilitaryNewsFA\nبه چت ملحق بشید:\n🔰 @MNChatFA",
    "خبرفوری"
  ),

    Language(
    "ru", # Russian
     -1001330302325, # https://t.me/MilitaryNewsRU
     "🔰 Подписывайтесь на @MilitaryNewsRU",
      "СРОЧНЫЕ_НОВОСТИ"
  ),

    Language(
    "pt", # Portugese
     -1001614849485, # https://t.me/MilitaryNewsBR
     "🔰 Se inscreva no @militaryNewsBR",
      "NOTÍCIAS_URGENTES"
  ),

    Language(
    "es", # Spanish
     -1001715032604, # https://t.me/MilitaryNewsES
     "🔰 Suscríbete a @MilitaryNewsES",
      "ÚLTIMA_HORA"
    )

]
