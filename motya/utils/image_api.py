import asyncio
import json
import logging
import os
from typing import Any

import aiohttp
from dotenv import load_dotenv


MAX_ATTEMPTS = 10
logger = logging.getLogger("text2img")


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.url = url
        self.auth_headers = {
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}",
        }

    async def _get_model(self, session: aiohttp.ClientSession):
        async with session.get(self.url + "key/api/v1/models") as response:
            data = await response.json()
        logger.info(f"using model {data[0]}")
        return data[0]["id"]

    async def _start_generate(
        self,
        session: aiohttp.ClientSession,
        form_data: aiohttp.FormData,
    ):
        async with session.post(
            self.url + "key/api/v1/text2image/run",
            data=form_data,
        ) as response:
            data = await response.json()
            logger.info(data)
        return data["uuid"]

    async def _check_generation(
        self,
        session: aiohttp.ClientSession,
        request_id: str,
        attempts: int = MAX_ATTEMPTS,
        delay_seconds: int = 10,
    ):
        while attempts > 0:
            logger.info(f"attempt: {MAX_ATTEMPTS - attempts + 1}")
            async with session.get(
                self.url + "key/api/v1/text2image/status/" + request_id
            ) as response:
                data = await response.json()

            if data["status"] == "DONE":
                return data["images"]

            attempts -= 1
            await asyncio.sleep(delay_seconds)

    def _create_form_data(self, params: dict[str, Any], model_id: int):
        form_data = aiohttp.FormData()
        form_data.add_field("model_id", str(model_id))
        form_data.add_field(
            "params",
            json.dumps(params),
            content_type="application/json",
            filename="blob",
        )
        return form_data

    async def generate_images(
        self,
        prompt: str,
        images_count: int = 1,
        width: int = 1024,
        height: int = 1024,
    ):
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            model_id = await self._get_model(session)
            params = {
                "type": "GENERATE",
                "numImages": images_count,
                "width": width,
                "height": height,
                "generateParams": {"query": prompt},
            }
            form_data = self._create_form_data(params, model_id)
            uuid = await self._start_generate(session, form_data)
            images = await self._check_generation(session, uuid)
        return images


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    API_KEY = os.getenv("FUSION_API_KEY")
    SECRET_KEY = os.getenv("FUSION_SECRET_KEY")
    api = Text2ImageAPI("https://api-key.fusionbrain.ai/", API_KEY, SECRET_KEY)
    images = asyncio.run(api.generate_images("house of blood"))
    print(images[0])
