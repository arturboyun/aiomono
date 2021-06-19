import logging
from datetime import datetime, timezone, timedelta
from typing import List, Union, Dict, Optional, Any

import aiohttp
from aiohttp import ClientResponse

from aiomono.exceptions import MonoException, ToManyRequests
from aiomono.signature import SignKey
from aiomono.types import Currency, ClientInfo, StatementItem
from aiomono.utils import validate_token, to_timestamp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mono')

API_ENDPOINT = 'https://api.monobank.ua'


class MonoClient:

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_currency(self) -> List[Currency]:
        """Returns list of courses"""
        currency_list = await self._get('/bank/currency')
        return [Currency(**currency) for currency in currency_list]

    async def _check_response(self, response: ClientResponse) -> Union[List, Dict]:
        logger.debug(f'({response.status}) Response: '
                     f'{await response.text()}, {await response.json()}, {response.headers}')
        if not response.ok:
            if response.status == 249:
                raise ToManyRequests(await response.text())
            raise MonoException(await response.text())
        return await response.json()

    async def _request(self, method, endpoint, **kwargs) -> Any:
        return await self._check_response(await self.session.request(method, API_ENDPOINT + endpoint, **kwargs))

    async def _get(self, endpoint: str, **kwargs) -> Union[List, Dict]:
        return await self._request('GET', endpoint, **kwargs)

    async def _post(self, endpoint: str, **kwargs) -> Union[List, Dict]:
        return await self._request('POST', endpoint, **kwargs)

    @property
    def session(self) -> aiohttp.ClientSession:
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        await self._session.close()

    def __enter__(self):
        raise RuntimeError('Use "async with" instead of simple "with" context manager')

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.close()


class PersonalMonoClient(MonoClient):
    def __init__(self, token: str):
        super().__init__()

        self.token = token
        self._headers = {'X-Token': self.token}

        validate_token(self.token)

    async def client_info(self) -> ClientInfo:
        """Returns client info"""
        client_info = await self._get('/personal/client-info', headers=self._headers)
        return ClientInfo(**client_info)

    async def set_webhook(self, webhook_url: str) -> bool:
        """Setting new webhook url"""
        payload = {"webHookUrl": webhook_url}
        response = await self._post('/personal/webhook', json=payload, headers=self._headers)
        return True

    async def get_statement(
            self,
            account_id: str,
            date_from: datetime = datetime.now(timezone.utc) - timedelta(days=31, hours=1),
            date_to: datetime = datetime.now(timezone.utc),
    ):
        """Returns list of statement items"""
        timestamp_from = to_timestamp(date_from)
        timestamp_to = to_timestamp(date_to)
        endpoint = f'/personal/statement/{account_id}/{timestamp_from}/{timestamp_to}'
        statement_items = await self._get(endpoint, headers=self._headers)
        return [StatementItem(**statement_item) for statement_item in statement_items]


class CorporateMonoClient(MonoClient):
    def __init__(self, request_id, private_key: str):
        super().__init__()

        self.request_id = request_id
        self.sign_key = SignKey(private_key)
        self._headers = {
            "X-Key-Id": self.sign_key.key_id(),
            "X-Time": to_timestamp(datetime.now()),
            "X-Request-Id": self.request_id,
        }

    def access_request(self, permissions: str = 'sp', callback_url: str = None):
        """Creates an access request for Corporate Monobank API user"""
        if 's' or 'p' in permissions:

        headers = {
            "X-Key-Id": self.sign_key.key_id(),
            "X-Time": to_timestamp(datetime.now()),
            "X-Permissions": permissions,
        }
        if callback_url:
            headers["X-Callback"] = callback_url
        sign_str = headers["X-Time"] + headers["X-Permissions"] + path
        headers["X-Sign"] = self.sign_key.sign(sign_str)
        return self._post('/personal/auth/request', headers=headers)
