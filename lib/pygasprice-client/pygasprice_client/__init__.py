# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2020 grandizzy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import threading
import time
from typing import Optional

import requests


class GasClientApi:
    """Asynchronous client for several gas price APIs.

    Creating an instance of this class runs a background thread, which fetches current
    recommended gas prices from gas price API every `refresh_interval` seconds. If due
    to network issues no current gas prices have been fetched for `expiry` seconds,
    old values expire and all `*_price()` methods will start returning `None` until
    the feed becomes available again.

    Also the moment before the first fetch has finished, all `*_price()` methods
    of this class return `None`.

    All gas prices are returned in Wei.

    Attributes:
        refresh_interval: Refresh frequency (in seconds).
        expiry: Expiration time (in seconds).
    """

    logger = logging.getLogger()

    def __init__(self, url: str, refresh_interval: int, expiry: int):
        assert(isinstance(url, str))
        assert(isinstance(refresh_interval, int))
        assert(isinstance(expiry, int))

        self.URL = url

        self.refresh_interval = refresh_interval
        self.expiry = expiry
        self._safe_low_price = None
        self._standard_price = None
        self._fast_price = None
        self._fastest_price = None
        self._suggest_base_fee = None
        self._last_refresh = 0
        self._expired = True
        threading.Thread(target=self._background_run, daemon=True).start()

    def _background_run(self):
        while True:
            self._fetch_price()
            time.sleep(self.refresh_interval)

    def _fetch_price(self):
        try:
            data = requests.get(self.URL).json()

            self._parse_api_data(data)
            self._last_refresh = int(time.time())

            self.logger.debug(f"Fetched current gas prices from {self.URL}: {data}")

            if self._expired:
                self.logger.info(f"Current gas prices information from {self.URL} became available")
                self._expired = False
        except:
            self.logger.warning(f"Failed to fetch current gas prices from {self.URL}")

    def _return_value_if_valid(self, value: int) -> Optional[int]:
        if int(time.time()) - self._last_refresh <= self.expiry:
            return value

        else:
            if self._last_refresh == 0:
                self.logger.warning(f"Current gas prices information from {self.URL} is unavailable")
                self._last_refresh = 1

            if not self._expired:
                self.logger.warning(f"Current gas prices information from {self.URL} has expired")
                self._expired = True

            return None

    def _parse_api_data(self, data):
        raise NotImplementedError

    def safe_low_price(self) -> Optional[int]:
        """Returns the current 'SafeLow (<30m)' gas price (in Wei).

        Returns:
            The current 'SafeLow (<30m)' gas price (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._safe_low_price)

    def standard_price(self) -> Optional[int]:
        """Returns the current 'Standard (<5m)' gas price (in Wei).

        Returns:
            The current 'Standard (<5m)' gas price (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._standard_price)

    def fast_price(self) -> Optional[int]:
        """Returns the current 'Fast (<2m)' gas price (in Wei).

        Returns:
            The current 'Fast (<2m)' gas price (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._fast_price)

    def fastest_price(self) -> Optional[int]:
        """Returns the current fastest (undocumented!) gas price (in Wei).

        Returns:
            The current fastest (undocumented!) gas price (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._fastest_price)


class GasClientApi1559:
    """Asynchronous client for several gas price APIs.

    Creating an instance of this class runs a background thread, which fetches current
    recommended gas prices from gas price API every `refresh_interval` seconds. If due
    to network issues no current gas prices have been fetched for `expiry` seconds,
    old values expire and all `*_price()` methods will start returning `None` until
    the feed becomes available again.

    Also the moment before the first fetch has finished, all `*_price()` methods
    of this class return `None`.

    All gas prices are returned in Wei.

    Attributes:
        refresh_interval: Refresh frequency (in seconds).
        expiry: Expiration time (in seconds).
    """

    logger = logging.getLogger()

    def __init__(self, url: str, refresh_interval: int, expiry: int):
        assert(isinstance(url, str))
        assert(isinstance(refresh_interval, int))
        assert(isinstance(expiry, int))

        self.URL = url

        self.refresh_interval = refresh_interval
        self.expiry = expiry
        self._safe_low_max_priority_fee = None
        self._standard_max_priority_fee = None
        self._fast_max_priority_fee = None
        self._fastest_max_priority_fee = None
        self._safe_low_max_fee = None
        self._standard_max_fee = None
        self._fast_max_fee = None
        self._fastest_max_fee = None
        self._last_refresh = 0
        self._expired = True
        threading.Thread(target=self._background_run, daemon=True).start()

    def _background_run(self):
        while True:
            self._fetch_price()
            time.sleep(self.refresh_interval)

    def _fetch_price(self):
        try:
            data = requests.get(self.URL).json()

            self._parse_api_data(data)
            self._last_refresh = int(time.time())

            self.logger.debug(f"Fetched current gas prices from {self.URL}: {data}")

            if self._expired:
                self.logger.info(f"Current gas prices information from {self.URL} became available")
                self._expired = False
        except:
            self.logger.warning(f"Failed to fetch current gas prices from {self.URL}")

    def _return_value_if_valid(self, value: int) -> Optional[int]:
        if int(time.time()) - self._last_refresh <= self.expiry:
            return value

        else:
            if self._last_refresh == 0:
                self.logger.warning(f"Current gas prices information from {self.URL} is unavailable")
                self._last_refresh = 1

            if not self._expired:
                self.logger.warning(f"Current gas prices information from {self.URL} has expired")
                self._expired = True

            return None

    def _parse_api_data(self, data):
        raise NotImplementedError

    def safe_low_max_priority_fee(self) -> Optional[int]:
        """Returns the current 'SafeLow (<30m)' max_priority_fee (in Wei).

        Returns:
            The current 'SafeLow (<30m)' max_priority_fee (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._safe_low_max_priority_fee)

    def standard_max_priority_fee(self) -> Optional[int]:
        """Returns the current 'Standard (<5m)' max_priority_fee (in Wei).

        Returns:
            The current 'Standard (<5m)' max_priority_fee (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._standard_max_priority_fee)

    def fast_max_priority_fee(self) -> Optional[int]:
        """Returns the current 'Fast (<2m)' max_priority_fee (in Wei).

        Returns:
            The current 'Fast (<2m)' max_priority_fee (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._fast_max_priority_fee)

    def fastest_max_priority_fee(self) -> Optional[int]:
        """Returns the current fastest (undocumented!) max_priority_fee (in Wei).

        Returns:
            The current fastest (undocumented!) max_priority_fee (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._fastest_max_priority_fee)

    def safe_low_max_fee(self) -> Optional[int]:
        """Returns the current 'SafeLow (<30m)' max_fee (in Wei).

        Returns:
            The current 'SafeLow (<30m)' max_fee (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._safe_low_max_fee)

    def standard_max_fee(self) -> Optional[int]:
        """Returns the current 'Standard (<5m)' max_fee (in Wei).

        Returns:
            The current 'Standard (<5m)' max_fee (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._standard_max_fee)

    def fast_max_fee(self) -> Optional[int]:
        """Returns the current 'Fast (<2m)' max_fee (in Wei).

        Returns:
            The current 'Fast (<2m)' max_fee (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._fast_max_fee)

    def fastest_max_fee(self) -> Optional[int]:
        """Returns the current fastest (undocumented!) max_fee (in Wei).

        Returns:
            The current fastest (undocumented!) max_fee (in Wei), or `None` if the client price
            feed has expired.
        """
        return self._return_value_if_valid(self._fastest_max_fee)


class EtherchainOrg(GasClientApi):

    URL = "https://www.etherchain.org/api/gasPriceOracle"
    SCALE = 1000000000

    def __init__(self, refresh_interval: int, expiry: int):
        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        self._safe_low_price = int(float(data['safeLow'])*self.SCALE)
        self._standard_price = int(float(data['standard'])*self.SCALE)
        self._fast_price = int(float(data['fast'])*self.SCALE)
        self._fastest_price = int(float(data['fastest'])*self.SCALE)

class Metamask(GasClientApi):

    URL = "https://api.metaswap.codefi.network/gasPrices"
    SCALE = 1000000000

    def __init__(self, refresh_interval: int, expiry: int):
        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        self._safe_low_price = int(float(data['SafeGasPrice'])*self.SCALE)
        self._standard_price = int(float(data['ProposeGasPrice'])*self.SCALE)
        self._fast_price = int(float(data['FastGasPrice'])*self.SCALE)
        self._fastest_price = int(float(data['FastGasPrice'])*self.SCALE)

class Metamask1559(GasClientApi1559):

    """
    {"low":{"suggestedMaxPriorityFeePerGas":"3","suggestedMaxFeePerGas":"53.323842299","minWaitTimeEstimate":15000,"maxWaitTimeEstimate":30000},"medium":{"suggestedMaxPriorityFeePerGas":"4","suggestedMaxFeePerGas":"62.711149349","minWaitTimeEstimate":15000,"maxWaitTimeEstimate":45000},"high":{"suggestedMaxPriorityFeePerGas":"5","suggestedMaxFeePerGas":"72.098456399","minWaitTimeEstimate":15000,"maxWaitTimeEstimate":60000},"estimatedBaseFee":"41.936535249"}
    """

    URL = "https://gas-api.metaswap.codefi.network/networks/1/suggestedGasFees"
    SCALE = 1000000000

    def __init__(self, refresh_interval: int, expiry: int):
        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        # MaxPriorityFeePerGas
        self._safe_low_max_priority_fee = int(float(data['low']['suggestedMaxPriorityFeePerGas'])*self.SCALE)
        self._standard_max_priority_fee = int(float(data['medium']['suggestedMaxPriorityFeePerGas'])*self.SCALE)
        self._fast_max_priority_fee = int(float(data['high']['suggestedMaxPriorityFeePerGas'])*self.SCALE)
        self._fastest_max_priority_fee = int(float(data['high']['suggestedMaxPriorityFeePerGas'])*self.SCALE)

        # MaxFeePerGas
        self._safe_low_max_fee = int(float(data['low']['suggestedMaxFeePerGas'])*self.SCALE)
        self._standard_max_fee = int(float(data['medium']['suggestedMaxFeePerGas'])*self.SCALE)
        self._fast_max_fee = int(float(data['high']['suggestedMaxFeePerGas'])*self.SCALE)
        self._fastest_max_fee = int(float(data['high']['suggestedMaxFeePerGas'])*self.SCALE)

        # Min/max wait times
        self._safe_low_min_wait_time = int(data['low']['minWaitTimeEstimate'])
        self._safe_low_max_wait_time = int(data['low']['maxWaitTimeEstimate'])
        self._standard_min_wait_time = int(data['medium']['minWaitTimeEstimate'])
        self._standard_max_wait_time = int(data['medium']['maxWaitTimeEstimate'])
        self._fast_min_wait_time = int(data['high']['minWaitTimeEstimate'])
        self._fast_max_wait_time = int(data['high']['maxWaitTimeEstimate'])
        self._fastest_min_wait_time = int(data['high']['minWaitTimeEstimate'])
        self._fastest_max_wait_time = int(data['high']['maxWaitTimeEstimate'])

class POANetwork(GasClientApi):

    URL = "https://gasprice.poa.network"
    SCALE = 1000000000

    def __init__(self, refresh_interval: int, expiry: int, alt_url=None):

        assert(isinstance(alt_url, str) or alt_url is None)

        if alt_url is not None:
            self.URL = alt_url

        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        self._safe_low_price = int(data['slow']*self.SCALE)
        self._standard_price = int(data['standard']*self.SCALE)
        self._fast_price = int(data['fast']*self.SCALE)
        self._fastest_price = int(data['instant']*self.SCALE)


class EthGasStation(GasClientApi):

    URL = "https://ethgasstation.info/json/ethgasAPI.json"
    SCALE = 100000000

    def __init__(self, refresh_interval: int, expiry: int, api_key=None):

        assert(isinstance(api_key, str) or api_key is None)

        if api_key is not None:
            self.URL = f"{self.URL}?api-key={api_key}"

        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        self._safe_low_price = int(data['safeLow']*self.SCALE)
        self._standard_price = int(data['average']*self.SCALE)
        self._fast_price = int(data['fast']*self.SCALE)
        self._fastest_price = int(data['fastest']*self.SCALE)


class Etherscan(GasClientApi):

    URL = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
    SCALE = 1000000000

    def __init__(self, refresh_interval: int, expiry: int, api_key=None):

        assert(isinstance(api_key, str) or api_key is None)

        if api_key is not None:
            self.URL = f"{self.URL}&apikey={api_key}"

        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        self._safe_low_price = int(data['result']['SafeGasPrice'])*self.SCALE
        self._standard_price = int(data['result']['ProposeGasPrice'])*self.SCALE
        self._fast_price = int(data['result']['FastGasPrice'])*self.SCALE
        self._fastest_price = int(data['result']['FastGasPrice'])*self.SCALE

class Polygonscan(GasClientApi):

    URL = "https://api.polygonscan.com/api?module=gastracker&action=gasoracle"
    SCALE = 1000000000

    def __init__(self, refresh_interval: int, expiry: int, api_key=None):

        assert(isinstance(api_key, str) or api_key is None)

        if api_key is not None:
            self.URL = f"{self.URL}&apikey={api_key}"

        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        self._safe_low_price = float(data['result']['SafeGasPrice'])*self.SCALE
        self._standard_price = float(data['result']['ProposeGasPrice'])*self.SCALE
        self._fast_price = float(data['result']['FastGasPrice'])*self.SCALE
        self._fastest_price = float(data['result']['FastGasPrice'])*self.SCALE
        self._suggest_base_fee = float(data['result']['suggestBaseFee'])*self.SCALE

class GasNow(GasClientApi):

    URL = "https://www.gasnow.org/api/v3/gas/price"
    SCALE = 1

    def __init__(self, refresh_interval: int, expiry: int, app_name=None):

        assert(isinstance(app_name, str) or app_name is None)

        if app_name is not None:
            self.URL = f"{self.URL}?utm_source={app_name}"

        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        self._safe_low_price = int(data['data']['slow'])*self.SCALE
        self._standard_price = int(data['data']['standard'])*self.SCALE
        self._fast_price = int(data['data']['fast'])*self.SCALE
        self._fastest_price = int(data['data']['rapid'])*self.SCALE

class EthGasWatch(GasClientApi):

    URL = "http://ethgas.watch/api/gas"
    SCALE = 1000000000

    def __init__(self, refresh_interval: int, expiry: int):

        self.URL = f"{self.URL}"

        super().__init__(self.URL, refresh_interval, expiry)

    def _parse_api_data(self, data):
        self._safe_low_price = int(data['slow']['gwei'])*self.SCALE
        self._standard_price = int(data['normal']['gwei'])*self.SCALE
        self._fast_price = int(data['fast']['gwei'])*self.SCALE
        self._fastest_price = int(data['instant']['gwei'])*self.SCALE
