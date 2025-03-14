# Импорт библиотек и классов
import aiohttp
import asyncio
import json
import config
import logging


async def convert_json_to_dict(input_string: str):
    """
    A function that converts JSON string to dictionary.

    Args:
        input_string (str): JSON string.

    Returns:
        dict: Returns JSON converted to dictionary
    """    
    input_string = input_string.replace('```json\n', '').replace('```', '')
    result_dict = dict(json.loads(input_string))
    return result_dict


### Генерация корзины полностью

async def generate_universal_mode(gender: str, age: str, budget: str, message_text: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a multipurpose assistant.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
    """    
    
    with open('goods/all_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот-консультант по умному подбору товаров в корзину на онлайн маркетплейсе. Твоя задача подобрать несколько товаров в json корзину покупателя так, чтобы не выйти за пределы бюджета покупателя. Подбирай максимально подходящие по критериям товары. Собранная корзина товаров должна представлять собой json файл. Ответь json файлом. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге.
В корзине должно быть не больше 10 товаров. Вот список доступных товаров в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Собери для меня корзину, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise


async def generate_food_mode(gender, age, budget, message_text):
    """
    А function that is responsible for generating a shopping cart on behalf of a nutritionist assistant.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
    """    
    with open('goods/food_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот json консультант-нутрициолог по умному подбору продуктов в корзину на онлайн маркетплейсе. Твоя задача подобрать несколько товаров в json корзину покупателя так, чтобы не выйти за пределы бюджета покупателя. Подбирай максимально подходящие по критериям товары. Собранная корзина товаров должна представлять собой json файл. Ответь json файлом. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот продукт]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот продукт]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге. Если запрос покупателя не соответствует ни одному товару в твоем каталоге и не подходит под твою специальность, как консультанта, вместо json корзины тебе нужно ответить json структурой с сообщением "not my specialty:
{
    "message": "not my specialty"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
В корзине должно быть не больше 10 товаров. Вот список доступных продуктов в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Собери для меня корзину, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise


async def generate_cloths_mode(gender: str, age: str, budget: str, message_text: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a stylist assistant.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
    """    
    with open('goods/cloths_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот json консультант-стилист по умному подбору одежды в корзину на онлайн маркетплейсе. Твоя задача подобрать несколько товаров в json корзину для нового образа покупателя так, чтобы не выйти за пределы бюджета покупателя. Подбирай максимально подходящие по критериям товары. Элементы образа должны быть гармоничными и дополнять друг-друга. Собранная корзина товаров должна представлять собой json файл. Ответь json файлом. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге. Если запрос покупателя не соответствует ни одному товару в твоем каталоге и не подходит под твою специальность, как консультанта, вместо json корзины тебе нужно ответить json структурой с сообщением "not my specialty:
{
    "message": "not my specialty"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
В корзине должно быть не больше 10 товаров. Вот список доступных товаров в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Собери для меня корзину, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise


async def generate_cosmetic_mode(gender: str, age: str, budget: str, message_text: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a cosmetologist assistant.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
    """    
    with open('goods/cosmetic_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот json консультант-косметолог по умному подбору товаров в корзину на онлайн маркетплейсе. Твоя задача подобрать несколько товаров в json корзину так, чтобы не выйти за пределы бюджета покупателя. Подбирай максимально подходящие по критериям товары. Собранная корзина товаров должна представлять собой json файл. Ответь json файлом. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге. Если запрос покупателя не соответствует ни одному товару в твоем каталоге и не подходит под твою специальность, как консультанта, вместо json корзины тебе нужно ответить json структурой с сообщением "not my specialty":
{
    "message": "not my specialty"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
В корзине должно быть не больше 10 товаров. Вот список доступных товаров в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Собери для меня корзину, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise


async def generate_decoration_mode(gender: str, age: str, budget: str, message_text: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a designer assistant.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
    """    
    with open('goods/decoration_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот json консультант-дизайнер по умному подбору в корзину товаров для декора на онлайн маркетплейсе. Твоя задача подобрать несколько товаров в json корзину так, чтобы не выйти за пределы бюджета покупателя. Подбирай максимально подходящие по критериям товары. Собранная корзина товаров должна представлять собой json файл. Ответь json файлом. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге. Если запрос покупателя не соответствует ни одному товару в твоем каталоге и не подходит под твою специальность, как консультанта, вместо json корзины тебе нужно ответить json структурой с сообщением "not my specialty":
{
    "message": "not my specialty"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
В корзине должно быть не больше 10 товаров. Вот список доступных товаров в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Собери для меня корзину, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise



### Генерация корзины с добавлением товара

async def generate_add_universal_mode(gender: str, age: str, budget: str, message_text: str, json_str_market_cart: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a multipurpose assistant with adding 1 item to the shopping cart.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
        json_str_market_cart (str): JSON string of all items in the shopping cart.
    """
    with open('goods/all_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот-консультант по умному подбору товаров в корзину на онлайн маркетплейсе. Твоя задача добавить товар в json корзину покупателя так, чтобы не выйти за пределы бюджета покупателя. Подбери максимально подходящий по критериям товар. Собранная корзина товаров должна представлять собой json файл. Ответь полным json файлом всей корзины пользователя, включив него добавленный товар. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар для добавления, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге.
В корзине должно быть не больше 10 товаров. Если в корзине уже 10 товаров и добавить больше нельзя, вместо json корзины тебе нужно ответить json структурой с сообщением "too many items":
{
    "message": "too many items"
}
Вот список доступных товаров в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Добавь мне в json корзину 1 товар так, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}. Вот моя json корзина в которую нужно добавить 1 товар:\n{json_str_market_cart}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise


async def generate_add_food_mode(gender: str, age: str, budget: str, message_text: str, json_str_market_cart: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a nutritionist assistant with adding 1 item to the shopping cart.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
        json_str_market_cart (str): JSON string of all items in the shopping cart.
    """
    with open('goods/food_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот json консультант-нутрициолог по умному подбору продуктов в корзину на онлайн маркетплейсе. Твоя задача добавить товар в json корзину покупателя так, чтобы не выйти за пределы бюджета покупателя. Подбери максимально подходящий по критериям товар. Собранная корзина товаров должна представлять собой json файл. Ответь полным json файлом всей корзины пользователя, включив него добавленный товар. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот продукт]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот продукт]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар для добавления, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге. Если запрос покупателя не соответствует ни одному товару в твоем каталоге и не подходит под твою специальность, как консультанта, вместо json корзины тебе нужно ответить json структурой с сообщением "not my specialty:
{
    "message": "not my specialty"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
В корзине должно быть не больше 10 товаров. Если в корзине уже 10 товаров и добавить больше нельзя, вместо json корзины тебе нужно ответить json структурой с сообщением "too many items":
{
    "message": "too many items"
}
Вот список доступных продуктов в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Добавь мне в json корзину 1 товар так, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}. Вот моя json корзина в которую нужно добавить 1 товар:\n{json_str_market_cart}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise


async def generate_add_cloths_mode(gender: str, age: str, budget: str, message_text: str, json_str_market_cart: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a stylist assistant with adding 1 item to the shopping cart.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
        json_str_market_cart (str): JSON string of all items in the shopping cart.
    """
    with open('goods/cloths_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот json консультант-стилист по умному подбору одежды в корзину на онлайн маркетплейсе. Твоя задача добавить товар в json корзину покупателя так, чтобы не выйти за пределы бюджета покупателя. Подбери максимально подходящий по критериям товар. Элементы образа должны быть гармоничными и дополнять друг-друга. Собранная корзина товаров должна представлять собой json файл. Ответь полным json файлом всей корзины пользователя, включив него добавленный товар. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар для добавления, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге. Если запрос покупателя не соответствует ни одному товару в твоем каталоге и не подходит под твою специальность, как консультанта, вместо json корзины тебе нужно ответить json структурой с сообщением "not my specialty:
{
    "message": "not my specialty"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
В корзине должно быть не больше 10 товаров. Если в корзине уже 10 товаров и добавить больше нельзя, вместо json корзины тебе нужно ответить json структурой с сообщением "too many items":
{
    "message": "too many items"
}
Вот список доступных товаров в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Добавь мне в json корзину 1 товар так, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}. Вот моя json корзина в которую нужно добавить 1 товар:\n{json_str_market_cart}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise


async def generate_add_cosmetic_mode(gender: str, age: str, budget: str, message_text: str, json_str_market_cart: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a cosmetologist assistant with adding 1 item to the shopping cart.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
        json_str_market_cart (str): JSON string of all items in the shopping cart.
    """
    with open('goods/cosmetic_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот json консультант-косметолог по умному подбору товаров в корзину на онлайн маркетплейсе. Твоя задача добавить товар в json корзину покупателя так, чтобы не выйти за пределы бюджета покупателя. Подбери максимально подходящий по критериям товар. Собранная корзина товаров должна представлять собой json файл. Ответь полным json файлом всей корзины пользователя, включив него добавленный товар. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар для добавления, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге. Если запрос покупателя не соответствует ни одному товару в твоем каталоге и не подходит под твою специальность, как консультанта, вместо json корзины тебе нужно ответить json структурой с сообщением "not my specialty":
{
    "message": "not my specialty"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
В корзине должно быть не больше 10 товаров. Если в корзине уже 10 товаров и добавить больше нельзя, вместо json корзины тебе нужно ответить json структурой с сообщением "too many items":
{
    "message": "too many items"
}
Вот список доступных товаров в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Добавь мне в json корзину 1 товар так, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}. Вот моя json корзина в которую нужно добавить 1 товар:\n{json_str_market_cart}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise


async def generate_add_decoration_mode(gender: str, age: str, budget: str, message_text: str, json_str_market_cart: str):
    """
    А function that is responsible for generating a shopping cart on behalf of a designer assistant with adding 1 item to the shopping cart.

    Args:
        gender (str): User gender.
        age (str): User age.
        budget (str): User budget.
        message_text (str): User request.
        json_str_market_cart (str): JSON string of all items in the shopping cart.
    """
    with open('goods/decoration_goods.csv', 'r', encoding='utf8') as f:
        presents_list = f.read()

    system_prompt = '''Ты - бот json консультант-дизайнер по умному подбору в корзину товаров для декора на онлайн маркетплейсе. Твоя задача добавить товар в json корзину покупателя так, чтобы не выйти за пределы бюджета покупателя. Подбери максимально подходящий по критериям товар. Собранная корзина товаров должна представлять собой json файл. Ответь полным json файлом всей корзины пользователя, включив него добавленный товар. Тебе запрещено писать что-либо вне json файла. Твой ответ должен представлять собой json файл такой структуры:
{
    "1": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    "2": {
        "message": "[объяснение покупателю, почему именно этот товар]",
        "id": "[id товара в каталоге]"
    },
    ...
}
Тебе запрещено использовать в объяснении покупателю id товара в каталоге. Пиши в поле "объяснение покупателю" только на русском языке, подробно и профессионально, используй эмодзи.
В одной позиции может быть строго 1 товар. Товары не должны повторяться. Запрещено, чтобы сумма стоимости всех товаров в корзине была больше, чем бюджет покупателя. Если бюджет покупателя слишком мал и не подходит ни под один товар для добавления, вместо json корзины тебе нужно ответить json структурой с сообщением "not enough money":
{
    "message": "not enough money"
}
Тебе разрешено добавлять в корзину только товары, которые есть в каталоге. Если запрос покупателя не соответствует ни одному товару в твоем каталоге и не подходит под твою специальность, как консультанта, вместо json корзины тебе нужно ответить json структурой с сообщением "not my specialty":
{
    "message": "not my specialty"
}
Если критерии покупателя неразборчивы, не относятся к сбору корзины или нецензурны, вместо json корзины тебе нужно ответить json структурой с сообщением "bad criteria":
{
    "message": "bad criteria"
}
В корзине должно быть не больше 10 товаров. Если в корзине уже 10 товаров и добавить больше нельзя, вместо json корзины тебе нужно ответить json структурой с сообщением "too many items":
{
    "message": "too many items"
}
Вот список доступных товаров в нашем каталоге:\n%s''' % (presents_list)
        
    start = f'Мой пол {gender}, мне {age} лет. Добавь мне в json корзину 1 товар так, чтобы ее суммарная стоимость было СТРОГО меньше моего бюджета {budget} рублей. Собери по этим критериям: {message_text}. Вот моя json корзина в которую нужно добавить 1 товар:\n{json_str_market_cart}'

    payload = json.dumps({
        "system_instruction": {
            "parts": {
                "text": system_prompt
            }
        },
        "contents": {
            "parts": {
                "text": start
            }
        },
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.8,
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    proxy_auth = aiohttp.BasicAuth(config.PROXY_LOGIN, config.PROXY_PASSWORD)

    for url in [config.GEMINI_URL]:
        for _ in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.post(url, headers=headers, data=payload, proxy=config.PROXY_IP, proxy_auth=proxy_auth, ssl=False)
                    result = dict(await response.json())

                result_dict = await convert_json_to_dict(result['candidates'][0]['content']['parts'][0]['text'])
                return result_dict
            
            except Exception as e:
                logging.exception('Gemini Не сгенерирован текст. Повтор генерации. Ошибка: ' + str(e))
                await asyncio.sleep(3)
    
    raise