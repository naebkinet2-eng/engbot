AUDITION_QUESTIONS = [
    {
        "id": "aud_1",
        "type": "choice",
        "prompt": "Консульский офицер спрашивает: 'What is the purpose of your trip to the United States?' Как ответить правильно для визы H-2B?",
        "options": [
            "I want to stay in America forever and find a rich wife.",
            "I am going to work temporarily as a seafood processor for one season and return home.",
            "I don't know, my friend bought me a ticket."
        ],
        "correct_index": 1
    },
    {
        "id": "aud_2",
        "type": "builder",
        "prompt": "Соберите фразу: «Я готов работать в ночную смену и брать переработки».",
        "words": ["I", "am", "ready", "to", "work", "night", "shifts", "and", "take", "overtime."],
        "answer": "I am ready to work night shifts and take overtime."
    },
    {
        "id": "aud_3",
        "type": "choice",
        "prompt": "Супервайзер в цеху кричит: 'Watch out! The floor is slippery near the conveyor!' Что это значит?",
        "options": [
            "Осторожно! Возле конвейера скользкий пол!",
            "Быстрее! Конвейер сломался, неси инструменты!",
            "Перерыв! Идем обедать в столовую!"
        ],
        "correct_index": 0
    }
]

MODULES = [
    {
        "id": "m1_embassy",
        "title": "1. Посольство США: Виза H-2B / H-2A",
        "tag": "Visa Interview",
        "description": "Как убедить консула в неиммиграционных намерениях и четко описать работу.",
        "dialogue": [
            {
                "speaker": "Officer",
                "tokens": [
                    ["Good", "Доброе"], ["morning.", "утро."], ["Why", "Почему"], ["are", "вы"],
                    ["you", "вы"], ["applying", "подаетесь"], ["for", "на"], ["an", "эту"],
                    ["H-2B", "H-2B"], ["visa?", "визу?"]
                ]
            },
            {
                "speaker": "You",
                "tokens": [
                    ["I", "Я"], ["have", "имею"], ["a", "официальный"], ["seasonal", "сезонный"],
                    ["job", "рабочий"], ["offer", "оффер"], ["at", "на"], ["a", "одном"],
                    ["seafood", "рыбоперерабатывающем"], ["plant", "заводе"], ["in", "на"],
                    ["Alaska.", "Аляске."]
                ]
            },
            {
                "speaker": "Officer",
                "tokens": [
                    ["What", "Какие"], ["ties", "связи"], ["do", "вы"], ["you", "имеете"],
                    ["have", "здесь"], ["to", "со"], ["your", "своей"], ["home", "родной"],
                    ["country?", "страной?"]
                ]
            },
            {
                "speaker": "You",
                "tokens": [
                    ["My", "Моя"], ["family", "семья"], ["and", "и"], ["college", "учеба"],
                    ["studies", "в колледже"], ["are", "находятся"], ["here,", "здесь,"],
                    ["so", "поэтому"], ["I", "я"], ["will", "вернусь"], ["return", "обратно"],
                    ["right", "сразу"], ["after", "после"], ["my", "моего"], ["contract.", "контракта."]
                ]
            }
        ],
        "builder": {
            "ru": "Я буду сортировать и упаковывать рыбу на конвейерной линии.",
            "words": ["I", "will", "sort", "and", "pack", "fish", "on", "the", "conveyor", "line."],
            "answer": "I will sort and pack fish on the conveyor line."
        },
        "speaking_prompt": "I am going to the United States for temporary seasonal work, and I will return home when my contract ends."
    },
    {
        "id": "m2_border",
        "title": "2. Граница США (CBP Control)",
        "tag": "Airport & Border",
        "description": "Прохождение паспортного контроля по прилету, документы I-797B и адрес работодателя.",
        "dialogue": [
            {
                "speaker": "CBP Officer",
                "tokens": [
                    ["Passport", "Паспорт"], ["and", "и"], ["petition", "петицию"],
                    ["approval", "одобрения"], ["notice,", "уведомление,"], ["please.", "пожалуйста."]
                ]
            },
            {
                "speaker": "You",
                "tokens": [
                    ["Here", "Вот"], ["is", "мой"], ["my", "паспорт"], ["passport", "и"],
                    ["and", "моя"], ["my", "форма"], ["I-797B", "I-797B"], ["form.", "документ."]
                ]
            },
            {
                "speaker": "CBP Officer",
                "tokens": [
                    ["Where", "Где"], ["will", "вы"], ["you", "будете"], ["be", "проживать"],
                    ["staying", "и"], ["and", "работать"], ["working?", "в США?"]
                ]
            },
            {
                "speaker": "You",
                "tokens": [
                    ["My", "Мой"], ["employer", "работодатель"], ["provides", "предоставляет"],
                    ["bunkhouse", "общежитие"], ["housing", "жилье"], ["right", "прямо"],
                    ["next", "рядом"], ["to", "с"], ["the", "заводом."], ["facility.", "предприятием."]
                ]
            }
        ],
        "builder": {
            "ru": "Я везу только личную одежду и никаких запрещенных продуктов.",
            "words": ["I", "am", "carrying", "only", "personal", "clothes", "and", "no", "restricted", "food."],
            "answer": "I am carrying only personal clothes and no restricted food."
        },
        "speaking_prompt": "Here are my passport and employer contract. My company provides housing near the processing plant."
    },
    {
        "id": "m3_seafood_plant",
        "title": "3. Рыбзавод и цех (Processing Line)",
        "tag": "Seafood Plant",
        "description": "Сленг и лексика цеха: slime line, филетирование, заморозка, темп линии.",
        "dialogue": [
            {
                "speaker": "Lead Worker",
                "tokens": [
                    ["Today", "Сегодня"], ["you", "ты"], ["are", "назначен"], ["assigned", "на"],
                    ["to", "линию"], ["the", "очистки"], ["slime", "рыбы"], ["line", "(slime line)"],
                    ["removing", "удаляя"], ["bloodlines.", "кровяные сгустки."]
                ]
            },
            {
                "speaker": "You",
                "tokens": [
                    ["Got", "Понял"], ["it.", "вас."], ["Should", "Нужно ли"], ["I", "мне"],
                    ["place", "класть"], ["cleaned", "очищенную"], ["salmon", "лосось"],
                    ["into", "в"], ["the", "синие"], ["blue", "контейнеры"], ["totes?", "ящики?"]
                ]
            },
            {
                "speaker": "Lead Worker",
                "tokens": [
                    ["Yes,", "Да,"], ["keep", "держи"], ["a", "стабильный"], ["steady", "темп"],
                    ["pace", "работы"], ["and", "и"], ["watch", "следи"], ["for", "за"],
                    ["damaged", "поврежденным"], ["fillets.", "филе."]
                ]
            }
        ],
        "builder": {
            "ru": "Холодильная камера заполнена поддонами с замороженной рыбой.",
            "words": ["The", "cold", "storage", "is", "full", "of", "pallets", "with", "frozen", "fish."],
            "answer": "The cold storage is full of pallets with frozen fish."
        },
        "speaking_prompt": "I understand the sorting rules. Should I move these full totes to the freezer line now?"
    },
    {
        "id": "m4_safety_ppe",
        "title": "4. Техника безопасности и экипировка (PPE)",
        "tag": "Safety First",
        "description": "Обязательная защита (hairnet, earplugs, rubber boots), травмы и остановка линии.",
        "dialogue": [
            {
                "speaker": "Safety Officer",
                "tokens": [
                    ["Never", "Никогда"], ["enter", "не входи"], ["the", "в"], ["wet", "мокрую"],
                    ["zone", "зону"], ["without", "без"], ["non-slip", "нескользящих"],
                    ["rubber", "резиновых"], ["boots", "сапог"], ["and", "и"], ["earplugs.", "берушей."]
                ]
            },
            {
                "speaker": "You",
                "tokens": [
                    ["My", "Моя"], ["cut-resistant", "порезостойкая"], ["glove", "перчатка"],
                    ["is", "порвана."], ["torn.", "повреждена."], ["Where", "Где"], ["can", "могу"],
                    ["I", "я"], ["grab", "взять"], ["a", "новую"], ["new", "запасную"], ["pair?", "пару?"]
                ]
            },
            {
                "speaker": "Safety Officer",
                "tokens": [
                    ["Ask", "Попроси"], ["the", "у"], ["floor", "цехового"], ["supervisor", "супервайзера"],
                    ["immediately", "немедленно"], ["before", "до того как"], ["touching", "трогать"],
                    ["any", "любой"], ["blades.", "нож / лезвие."]
                ]
            }
        ],
        "builder": {
            "ru": "Наденьте сетку для волос и фартук перед входом в цех.",
            "words": ["Put", "on", "your", "hairnet", "and", "apron", "before", "entering", "the", "floor."],
            "answer": "Put on your hairnet and apron before entering the floor."
        },
        "speaking_prompt": "Excuse me, I cut my rubber glove. I need a replacement pair before I continue working."
    },
    {
        "id": "m5_shifts_overtime",
        "title": "5. Смены, овертайм и общение с боссом",
        "tag": "Shifts & Overtime",
        "description": "Переработки (1.5x pay), отпроситься в туалет, сообщить о поломке или усталости.",
        "dialogue": [
            {
                "speaker": "Supervisor",
                "tokens": [
                    ["A", "Большое"], ["big", "рыболовное"], ["fishing", "судно"], ["boat", "лодка"],
                    ["just", "только что"], ["docked.", "пришвартовалось."], ["Can", "Можешь"],
                    ["you", "ты"], ["stay", "остаться"], ["four", "на четыре"], ["hours", "часа"],
                    ["overtime?", "сверхурочно?"]
                ]
            },
            {
                "speaker": "You",
                "tokens": [
                    ["Sure,", "Конечно,"], ["I", "я"], ["can", "могу"], ["do", "отработать"],
                    ["overtime.", "овертайм."], ["Can", "Можно"], ["I", "мне"], ["take", "взять"],
                    ["a", "короткий"], ["quick", "быстрый"], ["restroom", "туалетный"], ["break", "перерыв"],
                    ["first?", "сначала?"]
                ]
            },
            {
                "speaker": "Supervisor",
                "tokens": [
                    ["Yes,", "Да,"], ["let", "дай"], ["the", "сменщику"], ["relief", "подменному"],
                    ["worker", "рабочему"], ["cover", "подменить"], ["your", "твою"], ["spot.", "точку."]
                ]
            }
        ],
        "builder": {
            "ru": "Сверхурочная работа оплачивается в полуторном размере после сорока часов.",
            "words": ["Overtime", "is", "paid", "at", "time", "and", "a", "half", "after", "forty", "hours."],
            "answer": "Overtime is paid at time and a half after forty hours."
        },
        "speaking_prompt": "I am ready to work overtime today. Just let me know when my relief worker arrives."
    },
    {
        "id": "m6_bunkhouse_pay",
        "title": "6. Общежитие, зарплата и быт в США",
        "tag": "Daily Life",
        "description": "Чек/Direct Deposit, номер SSN, правила в bunkhouse, покупка еды и связи.",
        "dialogue": [
            {
                "speaker": "HR Coordinator",
                "tokens": [
                    ["Once", "Как только"], ["you", "ты"], ["get", "получишь"], ["your", "свой"],
                    ["Social", "номер"], ["Security", "социального"], ["Number,", "страхования (SSN),"],
                    ["we", "мы"], ["will", "настроим"], ["set", "прямой"], ["up", "перевод"],
                    ["direct", "на карту"], ["deposit.", "(direct deposit)."]
                ]
            },
            {
                "speaker": "You",
                "tokens": [
                    ["Thanks.", "Спасибо."], ["How", "Как"], ["much", "много"], ["is", "вычитается"],
                    ["deducted", "удерживается"], ["from", "из"], ["my", "моего"], ["paycheck", "зарплатного чека"],
                    ["for", "за"], ["room", "жилье"], ["and", "и"], ["board?", "питание?"]
                ]
            },
            {
                "speaker": "HR Coordinator",
                "tokens": [
                    ["Meals", "Питание"], ["and", "и"], ["housing", "жилье"], ["are", "полностью"],
                    ["free", "бесплатны"], ["as", "как"], ["stated", "указано"], ["in", "в"],
                    ["your", "твоем"], ["contract.", "контракте."]
                ]
            }
        ],
        "builder": {
            "ru": "Где я могу купить местную сим-карту и теплые носки?",
            "words": ["Where", "can", "I", "buy", "a", "local", "SIM", "card", "and", "warm", "socks?"],
            "answer": "Where can I buy a local SIM card and warm socks?"
        },
        "speaking_prompt": "Could you please explain the tax deductions on my first paycheck and when the shuttle goes to town?"
    }
]

INTERVIEW_QUESTIONS = [
    # 3 Вопроса от Консульского офицера (Посольство США)
    {
        "id": "int_1",
        "role": "Consular Officer (Посольство США)",
        "question": "Good morning. What exact job will you be performing in the United States, and who is your petitioning employer?",
        "hint_ru": "Назовите тип работы (например, seafood processor / seasonal worker), штат и что работа строго сезонная."
    },
    {
        "id": "int_2",
        "role": "Consular Officer (Посольство США)",
        "question": "Why should I believe that you will return to your home country after your H-2B contract expires instead of staying illegally?",
        "hint_ru": "Сделайте упор на учебу/семью/планы дома и уважение к визовым правилам США."
    },
    {
        "id": "int_3",
        "role": "Consular Officer (Посольство США)",
        "question": "How much money are you bringing with you for the first two weeks before you receive your first paycheck?",
        "hint_ru": "Ответьте уверенно: у вас есть сбережения на первое время, а жилье/питание описаны в контракте."
    },
    # 3 Вопроса от Американского работодателя (Рыбзавод / Сезонный супервайзер)
    {
        "id": "int_4",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "During peak fishing season, shifts can last 12 to 16 hours in cold, wet, and loud conditions. Tell me honestly—can you handle that physically?",
        "hint_ru": "Подчеркните физическую выносливость, опыт спорта/труда и готовность к длинным сменам."
    },
    {
        "id": "int_5",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "Imagine you are working on the processing line and you notice a piece of metal or a torn glove near the fish. What is your immediate action?",
        "hint_ru": "Правильный ответ: немедленно остановить/сообщить супервайзеру и не допустить загрязнения продукции."
    },
    {
        "id": "int_6",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "You will be living in a shared bunkhouse with coworkers from different countries. How do you deal with fatigue and conflicts on the job?",
        "hint_ru": "Покажите спокойствие, командный дух и фокус на работе и безопасности."
    }
]
