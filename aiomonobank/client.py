from typing import List, Any

import aiohttp
from aiohttp import ClientResponse

from aiomonobank.dataclasses import Currency

API_ENDPOINT = 'https://api.monobank.ua/'


class MonoClient:

    async def get_currency(self) -> List[Currency]:
        currency_list = await self._get('bank/currency')
        result = [Currency(**currency) for currency in await currency_list.json()]
        return result

    async def _parse_result(self, response: ClientResponse,):
        # todo:
        pass

    async def close(self):
        await self._session.close()

    async def _get(self, endpoint: str, **kwargs) -> ClientResponse:
        response = await self._session.get(API_ENDPOINT + endpoint, **kwargs)
        return response

    async def _post(self, endpoint: str, **kwargs) -> ClientResponse:
        response = await self._session.get(API_ENDPOINT + endpoint, **kwargs)
        return response

    def __enter__(self):
        raise RuntimeError('Use async with instead simple with')

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.close()


class PersonalMonoClient(MonoClient):
    pass


class CorporateMonoClient(MonoClient):
    pass
