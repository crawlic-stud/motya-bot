import asyncio
import base64
import json
import logging
import os
from typing import Any

import aiohttp
from dotenv import load_dotenv


MAX_ATTEMPTS = 20
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
        return data["uuid"], data.get("status_time")

    async def _check_generation(
        self,
        session: aiohttp.ClientSession,
        request_id: str,
        attempts: int = MAX_ATTEMPTS,
        delay_seconds: int = 10,
        estimated_time: int | None = None,
    ):
        if estimated_time:
            logger.info(f"Starting to generate. Estimated time is {estimated_time} seconds")

        while attempts > 0:
            async with session.get(self.url + "key/api/v1/text2image/status/" + request_id) as response:
                data = await response.json()

            current_attempt = MAX_ATTEMPTS - attempts + 1
            wait_delay = estimated_time if (current_attempt == 1 and estimated_time is not None) else delay_seconds
            logger.info(f"attempt: {current_attempt} / {MAX_ATTEMPTS}, status={data['status']}, {wait_delay=}")

            if data["status"] == "DONE":
                logger.info(f"DONE in {data.get('generationTime')} seconds")
                return data["images"]

            attempts -= 1
            await asyncio.sleep(wait_delay)
        logger.error(f"Generation failed.")

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

    @staticmethod
    def _decode_base64(base64_string: str) -> bytes:
        base64_img_bytes = base64_string.encode("utf-8")
        decoded_image_data = base64.b64decode(base64_img_bytes)
        return decoded_image_data

    async def generate_image(
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
            uuid, estimated_time = await self._start_generate(session, form_data)
            images = await self._check_generation(session, uuid, estimated_time=estimated_time)
        if images:
            return self._decode_base64(images[0])
