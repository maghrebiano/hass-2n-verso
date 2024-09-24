import aiohttp
import asyncio

class VersoAPI:
    def __init__(self, host, username, password):
        self._host = host
        self._username = username
        self._password = password
        self._session = aiohttp.ClientSession()

    async def get_system_info(self):
        url = f"http://{self._host}/api/system/info"
        async with self._session.get(url, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def get_system_status(self):
        url = f"http://{self._host}/api/system/status"
        async with self._session.get(url, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def get_switch_status(self, switch=None):
        url = f"http://{self._host}/api/switch/status"
        params = {}
        if switch is not None:
            params['switch'] = switch
        async with self._session.get(url, params=params, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def control_switch(self, switch, action, response=None, timeout=None):
        url = f"http://{self._host}/api/switch/ctrl"
        params = {
            'switch': switch,
            'action': action
        }
        if response is not None:
            params['response'] = response
        if timeout is not None:
            params['timeout'] = timeout
        async with self._session.get(url, params=params, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def get_call_status(self, session=None):
        url = f"http://{self._host}/api/call/status"
        params = {}
        if session is not None:
            params['session'] = session
        async with self._session.get(url, params=params, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def dial_call(self, number=None, users=None):
        url = f"http://{self._host}/api/call/dial"
        params = {}
        if number is not None:
            params['number'] = number
        if users is not None:
            params['users'] = users
        async with self._session.get(url, params=params, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def answer_call(self, session):
        url = f"http://{self._host}/api/call/answer"
        params = {'session': session}
        async with self._session.get(url, params=params, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def hangup_call(self, session, reason="normal"):
        url = f"http://{self._host}/api/call/hangup"
        params = {'session': session, 'reason': reason}
        async with self._session.get(url, params=params, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def get_camera_caps(self):
        url = f"http://{self._host}/api/camera/caps"
        async with self._session.get(url, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def get_camera_snapshot(self, width, height, source=None, fps=None, time=None):
        url = f"http://{self._host}/api/camera/snapshot"
        params = {
            'width': width,
            'height': height
        }
        if source is not None:
            params['source'] = source
        if fps is not None:
            params['fps'] = fps
        if time is not None:
            params['time'] = time
        async with self._session.get(url, params=params, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                return await response.read()
            else:
                response.raise_for_status()

    async def close(self):
        await self._session.close()
