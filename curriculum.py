import random

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

CONSULAR_QUESTION_POOL = [
    {
        "id": "con_1",
        "role": "Consular Officer (Посольство США)",
        "question": "Good morning. What exact job will you be performing in the United States, and who is your petitioning employer?",
        "tokens": [
            ["Good", "Доброе"], ["morning.", "утро."], ["What", "Какую"], ["exact", "именно"],
            ["job", "работу"], ["will", "будете"], ["you", "вы"], ["be", "выполнять"],
            ["performing", "делая"], ["in", "в"], ["the", "Соединенных"], ["United", "Штатах,"],
            ["States,", "США,"], ["and", "и"], ["who", "кто"], ["is", "является"],
            ["your", "вашим"], ["petitioning", "подающим петицию"], ["employer?", "работодателем?"]
        ],
        "hint_ru": "Назовите должность (seafood processor / seasonal worker), штат и что работа строго временная."
    },
    {
        "id": "con_2",
        "role": "Consular Officer (Посольство США)",
        "question": "Why should I believe that you will return to your home country after your H-2B contract expires instead of staying illegally?",
        "tokens": [
            ["Why", "Почему"], ["should", "должен"], ["I", "я"], ["believe", "верить,"],
            ["that", "что"], ["you", "вы"], ["will", "вернетесь"], ["return", "обратно"],
            ["to", "в"], ["your", "вашу"], ["home", "родную"], ["country", "страну"],
            ["after", "после того как"], ["your", "ваш"], ["H-2B", "H-2B"], ["contract", "контракт"],
            ["expires", "истечет"], ["instead", "вместо"], ["of", "того чтобы"],
            ["staying", "остаться"], ["illegally?", "нелегально?"]
        ],
        "hint_ru": "Укажите связи с домом: семья, учеба, планы и соблюдение визового закона США."
    },
    {
        "id": "con_3",
        "role": "Consular Officer (Посольство США)",
        "question": "How much money are you bringing with you for the first two weeks before you receive your first paycheck?",
        "tokens": [
            ["How", "Сколько"], ["much", "денег"], ["money", "средств"], ["are", "вы"],
            ["you", "вы"], ["bringing", "берете"], ["with", "с"], ["you", "собой"],
            ["for", "на"], ["the", "первые"], ["first", "две"], ["two", "недели"],
            ["weeks", "недель"], ["before", "до того как"], ["you", "вы"],
            ["receive", "получите"], ["your", "свой"], ["first", "первый"], ["paycheck?", "зарплатный чек?"]
        ],
        "hint_ru": "Ответьте уверенно: у вас есть сбережения на первое время, а жилье и питание описаны в контракте."
    },
    {
        "id": "con_4",
        "role": "Consular Officer (Посольство США)",
        "question": "How did you find this seasonal job in the United States, and did you pay any illegal recruitment fees?",
        "tokens": [
            ["How", "Как"], ["did", "вы"], ["you", "вы"], ["find", "нашли"],
            ["this", "эту"], ["seasonal", "сезонную"], ["job", "работу"], ["in", "в"],
            ["the", "США,"], ["United", "Соединенных"], ["States,", "Штатах,"], ["and", "и"],
            ["did", "платили ли"], ["you", "вы"], ["pay", "оплачивали"], ["any", "какие-либо"],
            ["illegal", "незаконные"], ["recruitment", "рекрутинговые"], ["fees?", "сборы/взносы?"]
        ],
        "hint_ru": "По закону H-2B работодатель сам оплачивает рекрутинг и петицию. Скажите, что подавались напрямую или через официальное агентство без незаконных сборов."
    },
    {
        "id": "con_5",
        "role": "Consular Officer (Посольство США)",
        "question": "Do you have any relatives or close friends currently living in the United States, and where are they located?",
        "tokens": [
            ["Do", "Имеете ли"], ["you", "вы"], ["have", "есть"], ["any", "каких-либо"],
            ["relatives", "родственников"], ["or", "или"], ["close", "близких"], ["friends", "друзей,"],
            ["currently", "в данный момент"], ["living", "живущих"], ["in", "в"],
            ["the", "США,"], ["United", "Соединенных"], ["States,", "Штатах,"], ["and", "и"],
            ["where", "где"], ["are", "они"], ["they", "они"], ["located?", "находятся?"]
        ],
        "hint_ru": "Отвечайте честно и спокойно: не скрывайте информацию, которая есть в анкете DS-160, и подчеркните, что вы едете только по своему контракту."
    },
    {
        "id": "con_6",
        "role": "Consular Officer (Посольство США)",
        "question": "What are your specific plans once your seasonal work contract ends in the autumn?",
        "tokens": [
            ["What", "Какие"], ["are", "есть"], ["your", "ваши"], ["specific", "конкретные"],
            ["plans", "планы,"], ["once", "как только"], ["your", "ваш"], ["seasonal", "сезонный"],
            ["work", "рабочий"], ["contract", "контракт"], ["ends", "закончится"], ["in", "осенью?"],
            ["the", "в"], ["autumn?", "осенний период?"]
        ],
        "hint_ru": "Опишите конкретные планы дома: продолжить учебу/работу, помочь семье, использовать заработанный опыт."
    },
    {
        "id": "con_7",
        "role": "Consular Officer (Посольство США)",
        "question": "Have you ever worked abroad before, and what is your current occupation or field of study at home?",
        "tokens": [
            ["Have", "Работали ли"], ["you", "вы"], ["ever", "когда-либо"], ["worked", "работали"],
            ["abroad", "за границей"], ["before,", "ранее,"], ["and", "и"], ["what", "какое"],
            ["is", "ваше"], ["your", "текущее"], ["current", "нынешнее"], ["occupation", "занятие/работа"],
            ["or", "или"], ["field", "направление"], ["of", "учебы"], ["study", "обучения"],
            ["at", "дома?"], ["home?", "на родине?"]
        ],
        "hint_ru": "Кратко расскажите о вашей учебе или текущей работе дома и опыте ответственности."
    },
    {
        "id": "con_8",
        "role": "Consular Officer (Посольство США)",
        "question": "What do you know about your employer's company and the city or state where you will be working?",
        "tokens": [
            ["What", "Что"], ["do", "вы"], ["you", "вы"], ["know", "знаете"],
            ["about", "о"], ["your", "вашего"], ["employer's", "работодателя"], ["company", "компании"],
            ["and", "и"], ["the", "городе"], ["city", "городе"], ["or", "или"],
            ["state", "штате,"], ["where", "где"], ["you", "вы"], ["will", "будете"],
            ["be", "быть"], ["working?", "работать?"]
        ],
        "hint_ru": "Покажите, что вы изучили работодателя: назовите сферу (переработка рыбы/морепродуктов), штат и условия проживания."
    },
    {
        "id": "con_9",
        "role": "Consular Officer (Посольство США)",
        "question": "What will you do if your employer offers you to stay longer after your H-2B visa expiration date?",
        "tokens": [
            ["What", "Что"], ["will", "будете"], ["you", "вы"], ["do", "делать,"],
            ["if", "если"], ["your", "ваш"], ["employer", "работодатель"], ["offers", "предложит"],
            ["you", "вам"], ["to", "остаться"], ["stay", "остаться"], ["longer", "дольше"],
            ["after", "после"], ["your", "вашей"], ["H-2B", "H-2B"], ["visa", "визы"],
            ["expiration", "окончания"], ["date?", "срока?"]
        ],
        "hint_ru": "Единственно верный ответ: я обязан покинуть США до истечения срока визы/I-94, чтобы не нарушать закон и иметь право приехать в будущем."
    },
    {
        "id": "con_10",
        "role": "Consular Officer (Посольство США)",
        "question": "Who is paying for your flight tickets to the United States and your visa application fees?",
        "tokens": [
            ["Who", "Кто"], ["is", "оплачивает"], ["paying", "платит"], ["for", "за"],
            ["your", "ваши"], ["flight", "авиа"], ["tickets", "билеты"], ["to", "в"],
            ["the", "США"], ["United", "Соединенные"], ["States", "Штаты"], ["and", "и"],
            ["your", "ваши"], ["visa", "визовые"], ["application", "заявочные"], ["fees?", "сборы?"]
        ],
        "hint_ru": "Уточните, что согласно правилам программы H-2B работодатель возмещает транспортные расходы или оплачивает перелет, а у вас есть личные средства на дорожные расходы."
    },
    {
        "id": "con_11",
        "role": "Consular Officer (Посольство США)",
        "question": "Why are you choosing temporary manual labor in the US instead of finding a job in your own specialty at home?",
        "tokens": [
            ["Why", "Почему"], ["are", "вы"], ["you", "вы"], ["choosing", "выбираете"],
            ["temporary", "временный"], ["manual", "физический"], ["labor", "труд"], ["in", "в"],
            ["the", "США"], ["US", "Америке"], ["instead", "вместо"], ["of", "того чтобы"],
            ["finding", "найти"], ["a", "работу"], ["job", "работу"], ["in", "по"],
            ["your", "вашей"], ["own", "собственной"], ["specialty", "специальности"], ["at", "дома?"],
            ["home?", "на родине?"]
        ],
        "hint_ru": "Объясните, что это отличная возможность попрактиковать английский, поработать в международной команде и заработать стартовый капитал за один сезон."
    },
    {
        "id": "con_12",
        "role": "Consular Officer (Посольство США)",
        "question": "Do you understand your rights as a temporary worker in the United States under the Wilberforce pamphlet?",
        "tokens": [
            ["Do", "Понимаете ли"], ["you", "вы"], ["understand", "понимаете"], ["your", "ваши"],
            ["rights", "права"], ["as", "как"], ["a", "временного"], ["temporary", "сезонного"],
            ["worker", "работника"], ["in", "в"], ["the", "США"], ["United", "Соединенных"],
            ["States", "Штатах"], ["under", "согласно"], ["the", "брошюре"],
            ["Wilberforce", "Уилберфорса"], ["pamphlet?", "(памятке о правах)?"]
        ],
        "hint_ru": "Скажите: да, я прочитал памятку, знаю свои права на безопасные условия труда, честную оплату и право хранить свой паспорт при себе."
    }
]

EMPLOYER_QUESTION_POOL = [
    {
        "id": "emp_1",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "During peak fishing season, shifts can last 12 to 16 hours in cold, wet, and loud conditions. Tell me honestly—can you handle that physically?",
        "tokens": [
            ["During", "Во время"], ["peak", "пикового"], ["fishing", "рыболовного"], ["season,", "сезона,"],
            ["shifts", "смены"], ["can", "могут"], ["last", "длиться"], ["12", "12"],
            ["to", "до"], ["16", "16"], ["hours", "часов"], ["in", "в"],
            ["cold,", "холодных,"], ["wet,", "мокрых,"], ["and", "и"], ["loud", "шумных"],
            ["conditions.", "условиях."], ["Tell", "Скажи"], ["me", "мне"], ["honestly—can", "честно — сможешь ли"],
            ["you", "ты"], ["handle", "справиться с"], ["that", "этим"], ["physically?", "физически?"]
        ],
        "hint_ru": "Подчеркните физическую выносливость, регулярные тренировки/спорт и готовность к долгим сменам на ногах."
    },
    {
        "id": "emp_2",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "Imagine you are working on the processing line and you notice a piece of metal or a torn glove near the fish. What is your immediate action?",
        "tokens": [
            ["Imagine", "Представь,"], ["you", "ты"], ["are", "работаешь"], ["working", "работая"],
            ["on", "на"], ["the", "перерабатывающей"], ["processing", "производственной"], ["line", "линии"],
            ["and", "и"], ["you", "ты"], ["notice", "замечаешь"], ["a", "кусок"],
            ["piece", "фрагмент"], ["of", "металла"], ["metal", "металла"], ["or", "или"],
            ["a", "порванную"], ["torn", "рваную"], ["glove", "перчатку"], ["near", "рядом с"],
            ["the", "рыбой."], ["fish.", "рыбой."], ["What", "Какое"], ["is", "твое"],
            ["your", "твоё"], ["immediate", "немедленное"], ["action?", "действие?"]
        ],
        "hint_ru": "Правильный ответ: немедленно сообщить супервайзеру / остановить участок, чтобы не допустить загрязнения продукции."
    },
    {
        "id": "emp_3",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "You will be living in a shared bunkhouse with coworkers from different countries. How do you deal with fatigue and conflicts on the job?",
        "tokens": [
            ["You", "Ты"], ["will", "будешь"], ["be", "жить"], ["living", "проживая"],
            ["in", "в"], ["a", "общем"], ["shared", "совместном"], ["bunkhouse", "общежитии"],
            ["with", "с"], ["coworkers", "коллегами"], ["from", "из"], ["different", "разных"],
            ["countries.", "стран."], ["How", "Как"], ["do", "ты"], ["you", "ты"],
            ["deal", "справляешься"], ["with", "с"], ["fatigue", "усталостью"], ["and", "и"],
            ["conflicts", "конфликтами"], ["on", "на"], ["the", "работе?"], ["job?", "рабочем месте?"]
        ],
        "hint_ru": "Покажите спокойствие, уважение к чужому отдыху и фокус на работе без ссор."
    },
    {
        "id": "emp_4",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "If the conveyor belt is moving too fast and fish is piling up at your station, what will you say and do?",
        "tokens": [
            ["If", "Если"], ["the", "конвейерная"], ["conveyor", "лента"], ["belt", "конвейера"],
            ["is", "движется"], ["moving", "двигаясь"], ["too", "слишком"], ["fast", "быстро"],
            ["and", "и"], ["fish", "рыба"], ["is", "накапливается"], ["piling", "скапливаясь"],
            ["up", "в кучу"], ["at", "на"], ["your", "твоей"], ["station,", "станции,"],
            ["what", "что"], ["will", "будешь"], ["you", "ты"], ["say", "говорить"],
            ["and", "и"], ["do?", "делать?"]
        ],
        "hint_ru": "Не паниковать и не бросать пост: сразу подать сигнал бригадиру (Lead Worker), чтобы помогли разгрузить линию."
    },
    {
        "id": "emp_5",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "We have zero tolerance for alcohol, drugs, and skipping safety gear on the plant floor. Are you okay with strict daily inspections?",
        "tokens": [
            ["We", "У нас"], ["have", "есть"], ["zero", "нулевая"], ["tolerance", "терпимость"],
            ["for", "к"], ["alcohol,", "алкоголю,"], ["drugs,", "наркотикам,"], ["and", "и"],
            ["skipping", "игнорированию"], ["safety", "защитной"], ["gear", "экипировки"], ["on", "в"],
            ["the", "цеху."], ["plant", "заводском"], ["floor.", "помещении."], ["Are", "Согласен ли"],
            ["you", "ты"], ["okay", "согласен"], ["with", "со"], ["strict", "строгими"],
            ["daily", "ежедневными"], ["inspections?", "проверками?"]
        ],
        "hint_ru": "Ответьте твердо: да, я полностью поддерживаю дисциплину, трезвость и правила техники безопасности."
    },
    {
        "id": "emp_6",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "Sometimes a fishing boat arrives at 3 AM and we call workers for an emergency unloading shift. How fast can you wake up and report to duty?",
        "tokens": [
            ["Sometimes", "Иногда"], ["a", "рыболовное"], ["fishing", "рыболовецкое"], ["boat", "судно"],
            ["arrives", "прибывает"], ["at", "в"], ["3", "3"], ["AM", "часа ночи"],
            ["and", "и"], ["we", "мы"], ["call", "вызываем"], ["workers", "рабочих"],
            ["for", "на"], ["an", "экстренную"], ["emergency", "срочную"], ["unloading", "разгрузочную"],
            ["shift.", "смену."], ["How", "Как"], ["fast", "быстро"], ["can", "можешь"],
            ["you", "ты"], ["wake", "проснуться"], ["up", "встать"], ["and", "и"],
            ["report", "явиться"], ["to", "на"], ["duty?", "смену?"]
        ],
        "hint_ru": "Скажите, что держите форму рядом, не опаздываете и готовы выйти на смену через 15–20 минут после вызова."
    },
    {
        "id": "emp_7",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "Have you ever worked with sharp knives, heavy boxes, or industrial machinery before?",
        "tokens": [
            ["Have", "Работал ли"], ["you", "ты"], ["ever", "когда-либо"], ["worked", "работал"],
            ["with", "с"], ["sharp", "острыми"], ["knives,", "ножами,"], ["heavy", "тяжелыми"],
            ["boxes,", "коробками,"], ["or", "или"], ["industrial", "промышленным"],
            ["machinery", "оборудованием"], ["before?", "ранее?"]
        ],
        "hint_ru": "Опишите любой опыт физического труда, работы с инструментами или спортивной работы с весами и внимательность к безопасности."
    },
    {
        "id": "emp_8",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "What would you do if you accidentally cut your finger or felt dizzy while working in the cold freezer room?",
        "tokens": [
            ["What", "Что"], ["would", "бы"], ["you", "ты"], ["do", "сделал,"],
            ["if", "если"], ["you", "ты"], ["accidentally", "случайно"], ["cut", "порезал"],
            ["your", "свой"], ["finger", "палец"], ["or", "или"], ["felt", "почувствовал"],
            ["dizzy", "головокружение"], ["while", "во время"], ["working", "работы"], ["in", "в"],
            ["the", "холодной"], ["cold", "морозильной"], ["freezer", "камере"], ["room?", "помещении?"]
        ],
        "hint_ru": "Немедленно предупредить подменного/супервайзера, выйти с линии и обратиться в медпункт (First Aid), чтобы не занести инфекцию в рыбу."
    },
    {
        "id": "emp_9",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "Some tasks like cleaning fish guts on the slime line or stacking 50-pound frozen cases are repetitive. How do you stay focused?",
        "tokens": [
            ["Some", "Некоторые"], ["tasks", "задачи"], ["like", "такие как"], ["cleaning", "очистка"],
            ["fish", "рыбьих"], ["guts", "внутренностей"], ["on", "на"], ["the", "линии"],
            ["slime", "очистки"], ["line", "(slime line)"], ["or", "или"], ["stacking", "укладка"],
            ["50-pound", "50-фунтовых (~22 кг)"], ["frozen", "замороженных"], ["cases", "коробок"],
            ["are", "являются"], ["repetitive.", "однообразными."], ["How", "Как"], ["do", "ты"],
            ["you", "ты"], ["stay", "сохраняешь"], ["focused?", "концентрацию?"]
        ],
        "hint_ru": "Скажите, что воспринимаете монотонную работу как тренировку выносливости, следите за качеством каждого движения и мотивированы заработком."
    },
    {
        "id": "emp_10",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "If you do not understand an instruction from your team leader in a noisy room, how will you respond?",
        "tokens": [
            ["If", "Если"], ["you", "ты"], ["do", "не"], ["not", "не"],
            ["understand", "понимаешь"], ["an", "инструкцию"], ["instruction", "указание"], ["from", "от"],
            ["your", "твоего"], ["team", "бригадира"], ["leader", "лидера"], ["in", "в"],
            ["a", "шумном"], ["noisy", "громком"], ["room,", "цеху,"], ["how", "как"],
            ["will", "будешь"], ["you", "ты"], ["respond?", "реагировать?"]
        ],
        "hint_ru": "Никогда не кивать впустую: переспросить ('Could you please repeat or show me once?') и убедиться, что понял задачу на 100%."
    },
    {
        "id": "emp_11",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "Why should we hire you over other seasonal applicants from around the world?",
        "tokens": [
            ["Why", "Почему"], ["should", "должны"], ["we", "мы"], ["hire", "нанять"],
            ["you", "тебя"], ["over", "вместо"], ["other", "других"], ["seasonal", "сезонных"],
            ["applicants", "кандидатов"], ["from", "со"], ["around", "всего"], ["the", "мира?"],
            ["world?", "света?"]
        ],
        "hint_ru": "Назовите 3 сильные стороны: отличная физическая форма, надежность без прогулов и умение быстро учиться."
    },
    {
        "id": "emp_12",
        "role": "US Plant Supervisor (Работодатель, США)",
        "question": "Are you prepared to stay until the very end of the contract even if the weather is bad and the work is tough?",
        "tokens": [
            ["Are", "Готов ли"], ["you", "ты"], ["prepared", "подготовлен"], ["to", "остаться"],
            ["stay", "работать"], ["until", "до"], ["the", "самого"], ["very", "самого"],
            ["end", "конца"], ["of", "контракта,"], ["the", "этого"], ["contract", "договора,"],
            ["even", "даже"], ["if", "если"], ["the", "погода"], ["weather", "погода"],
            ["is", "плохая"], ["bad", "суровая"], ["and", "и"], ["the", "работа"],
            ["work", "труд"], ["is", "тяжелая?"], ["tough?", "сложная?"]
        ],
        "hint_ru": "Подтвердите, что вы человек слова и доведете контракт до конца независимо от погоды и нагрузки."
    }
]


def get_random_interview_set() -> list[dict]:
    consular = random.sample(CONSULAR_QUESTION_POOL, 3)
    employer = random.sample(EMPLOYER_QUESTION_POOL, 3)
    return consular + employer


INTERVIEW_QUESTIONS = get_random_interview_set()
