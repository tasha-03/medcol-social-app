STUDENT_RECORD_FIELDS = [
    "id",
    "fio",
    "birthdate",
    "addedByUser",
    "groupId",
    "deleted",
    "modifiedByUser",
    "lastModified",
    "registration",
    "refugee",
    "dormitory",
    "living",
    "socialStatusFamily",
    "parents",
    "parentsJob",
    "socialStatusStudentOrphan",
    "socialStatusStudentInvalid",
    "studentFamily",
    "studentFamilyChildren",
    "scholarship",
    "transport",
    "transportPass",
    "svo",
    "svoChild",
    "svoParent",
    "studentRisk",
    "statusStudy",
    "note"
]

STUDENT_STRUCTURE = {
    "id": {
        "label": "Идентификатор",
        "type": "int",
        "modifiers": ["PRIMARY KEY"]
    },
    "fio": {
        "label": "ФИО",
        "type": "str"
    },
    "birthdate": {
        "label": "Дата рождения",
        "type": "str"
    },
    "addedByUser": {
        "label": "Добавлено пользователем",
        "type": "int",
        "modifiers": ["FOREIGN KEY"]
    },
    "groupId": {
        "label": "Группа",
        "type": "int",
        "modifiers": ["FOREIGN KEY"]
    },
    "deleted": {
        "label": "Удалено",
        "type": "check",
        "allowed values": [
            0,
            1
        ]
    },
    "modifiedByUser": {
        "label": "Изменено пользователем",
        "type": "int",
        "modifiers": ["FOREIGN KEY"]
    },
    "lastModified": {
        "label": "Изменено",
        "type": "str"
    },

    # actual fields
    "fields": {
        "Проживание": {
            "registration": {
                "label": "Прописка",
                "labelShort": "Прописка",
                "type": "str",
                "allowed values": [
                    "г. Владимир",
                    "город Владимирской области",
                    "район Владимирской области",
                    "Не Владимирская область"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Не указано"
            },
            "refugee": {
                "label": "Статус студента (переселенец/беженец)",
                "labelShort": "Переселенец/беженец",
                "type": "str",
                "allowed values": [
                    "ДНР",
                    "ЛНР",
                    "Херсонская область",
                    "Курская область"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
            "dormitory": {
                "label": "Нуждается в общежитии",
                "labelShort": "Нуждается в общежитии",
                "type": "check",
                "allowed values": [
                    0,
                    1
                ],
                "modifiers": ["FILTER"]
            },
            "living": {
                "label": "Проживание",
                "labelShort": "Проживание",
                "type": "str",
                "allowed values": [
                    "Съемное жильё",
                    "Общежитие ОУ",
                    "Собственное жилье"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Не указано"
            },
        },
        "Социальный статус": {
            "socialStatusFamily": {
                "label": "Социальный статус семьи",
                "labelShort": "Социальный статус семьи",
                "type": "str",
                "allowed values": [
                    "Полная",
                    "Неполная",
                    "Многодетная (при наличии справки)",
                    "Малообеспеченная (при наличии справки)"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Не указано"
            },
            "parents": {
                "label": "Родители/законные представители",
                "labelShort": "Родители/законные представители",
                "type": "str",
                "allowed values": [
                    "Мать + Отец",
                    "Мать + Отчим",
                    "Отец + Мачеха",
                    "Отчим + Мачеха",
                    "Мать",
                    "Отец",
                    "Мачеха",
                    "Отчим",
                    "Нет"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Не указано"
            },
            "parentsJob": {
                "label": "Трудоустройство родителей",
                "labelShort": "Трудоустройство родителей",
                "type": "str",
                "allowed values": [
                    "Мать (мачеха)",
                    "Отец (отчим)",
                    "Оба",
                    "Никто"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Не указано"
            },
            "socialStatusStudentOrphan": {
                "label": "Социальный статус студента (сирота)",
                "labelShort": "Сирота",
                "type": "str",
                "allowed values": [
                    "Сирота (Гособеспечение)",
                    "Сирота (Опека)"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
            "socialStatusStudentInvalid": {
                "label": "Социальный статус студента (инвалид, ЛОВЗ)",
                "labelShort": "Инвалидность/ЛОВЗ",
                "type": "str",
                "allowed values": [
                    "Инвалид детства",
                    "Ребенок инвалид",
                    "Инвалид",
                    "Лица с ограниченными возможностями здоровья"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
            "studentFamily": {
                "label": "Студенческая семья (обучающиеся ВБМК на очной форме обучения)",
                "labelShort": "Студенческая семья (очно)",
                "type": "str",
                "allowed values": [
                    "Да (полная семья)",
                    "Да (неполная семья)"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
            "studentFamilyChildren": {
                "label": "Студенческая семья (количество детей)",
                "labelShort": "Количество детей",
                "type": "int",
                "modifiers": ["NULLABLE"],
                "nullValueLabel": "Нет"
            },
            "scholarship": {
                "label": "Стипендия",
                "labelShort": "Стипендия",
                "type": "str",
                "allowed values": [
                    "академическая",
                    "социальная"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
        },
        "Транспорт": {
            "transport": {
                "label": "Использование транспорта",
                "labelShort": "Использование транспорта",
                "type": "str",
                "allowed values": [
                    "Городской",
                    "Пригородный",
                    "Железнодорожный"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
            "transportPass": {
                "label": "Использование транспорта (проездной)",
                "labelShort": "Проездной",
                "type": "check",
                "allowed values": [
                    0,
                    1
                ],
                "modifiers": ["FILTER"]
            },
        },
        "СВО": {
            "svo": {
                "label": "Студент участник/ветеран военных конфликтов",
                "labelShort": "Студент участник/ветеран военных конфликтов",
                "type": "str",
                "allowed values": [
                    "СВО",
                    "Другие"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
            "svoChild": {
                "label": "Дети участников СВО",
                "labelShort": "Дети участников СВО",
                "type": "check",
                "allowed values": [
                    0,
                    1
                ],
                "modifiers": ["FILTER"]
            },
            "svoParent": {
                "label": "Степень родства детей участников СВО",
                "labelShort": "Родство участников СВО",
                "type": "str",
                "allowed values": [
                    "Мать (мачеха)",
                    "Отец (отчим)"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
        },
        "Статус студента": {
            "studentRisk": {
                "label": "Студент группы риска",
                "labelShort": "Студент группы риска",
                "type": "str",
                "allowed values": [
                    "Состоящие на учете в ОДН",
                    "Состоящие на учете в КДН",
                    "Внутриколледжный учёт"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Нет"
            },
            "statusStudy": {
                "label": "Статус обучающегося",
                "labelShort": "Статус обучающегося",
                "type": "str",
                "allowed values": [
                    "Отчислен",
                    "Академический отпуск",
                    "Прочее"
                ],
                "modifiers": ["NULLABLE", "FILTER"],
                "nullValueLabel": "Обучается"
            },
        },
        "Прочее": {
            "note": {
                "label": "Примечание",
                "labelShort": "Примечание",
                "type": "str"
            },
        }
    }
}

STUDENT_FIELDSETS_FILTER = {}
for k,v in STUDENT_STRUCTURE["fields"].items():
    for k1,v1 in v.items():
        STUDENT_FIELDSETS_FILTER[k] = ""
        if "FILTER" in v1.get("modifiers", []):
            STUDENT_FIELDSETS_FILTER[k] = "FILTER"

STUDENT_FIELDS = {}
for k,v in STUDENT_STRUCTURE.items():
    if k != "fields":
        STUDENT_FIELDS[k] = v

for k,v in STUDENT_STRUCTURE["fields"].items():
    for k1, v1 in v.items():
        STUDENT_FIELDS[k1] = v1

if __name__ == "__main__":
    print(STUDENT_FIELDSETS_FILTER)