from misc.config import YANDEX_GPT_CATALOG_ID, YANDEX_GPT_API_KEY, YANDEX_GPT_MODEL_TYPE

from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey

# TODO: Убрать модуль yandex_gpt внутрь integrations
config_manager = YandexGPTConfigManagerForAPIKey(
    model_type=YANDEX_GPT_MODEL_TYPE,
    catalog_id=YANDEX_GPT_CATALOG_ID,
    api_key=YANDEX_GPT_API_KEY
)
yandex_gpt = YandexGPT(config_manager=config_manager)

async def moderate_text(text: str) -> bool:
    # TODO: Сделать кеширование матных слов, дабы не делать каждый раз попусту запрос на одно и то же слово.
    completion = await yandex_gpt.get_async_completion(
        messages=[
            {"role": "system", "text": "Привет, твоя задача найти в тексте нецензурную брань и вернуть 1, если она найдена. В противном случае - 0."},
            {"role": "user", "text": text}
        ]
    )

    return bool(int(completion))
