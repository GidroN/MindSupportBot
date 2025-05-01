from misc.config import YANDEX_GPT_CATALOG_ID, YANDEX_GPT_API_KEY, YANDEX_GPT_MODEL_TYPE
from . import YandexGPT, YandexGPTConfigManagerForAPIKey

config_manager = YandexGPTConfigManagerForAPIKey(
    model_type=YANDEX_GPT_MODEL_TYPE,
    catalog_id=YANDEX_GPT_CATALOG_ID,
    api_key=YANDEX_GPT_API_KEY
)
yandex_gpt = YandexGPT(config_manager=config_manager)


async def moderate_text(text: str, timeout: int = 20) -> bool:
    system_text = "Привет, твоя задача найти в тексте нецензурную брань (мат, пошлости и прочая сильная цензура) и вернуть 1, если она найдена. В противном случае - 0."
    completion = await yandex_gpt.get_async_completion(
        messages=[
            {"role": "system", "text": system_text},
            {"role": "user", "text": text}
        ],
        timeout=timeout,
        max_tokens=3000
    )

    return bool(int(completion))
