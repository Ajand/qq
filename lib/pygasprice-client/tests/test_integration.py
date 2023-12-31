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
import time

import pytest

from pygasprice_client import Metamask, EthGasStation, POANetwork, EtherchainOrg, Etherscan, GasNow, EthGasWatch
from pygasprice_client import Polygonscan


@pytest.mark.timeout(45)
@pytest.mark.skip
def test_poanetwork_integration():
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)

    poa = POANetwork(10, 600)

    while True:
        safe_low_price = poa.safe_low_price()
        logging.info(safe_low_price)

        standard_price = poa.standard_price()
        logging.info(standard_price)

        fast_price = poa.fast_price()
        logging.info(fast_price)

        if safe_low_price is not None and standard_price is not None and fast_price is not None:
            break

        time.sleep(1)

def test_custom_poa_url():
    local_poa = POANetwork(10, 600, "http://127.0.0.1:8000")
    assert local_poa.URL == "http://127.0.0.1:8000"

    local_poa = POANetwork(10, 600)
    assert local_poa.URL == "https://gasprice.poa.network"


@pytest.mark.timeout(45)
def test_etherchain_integration():
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)

    etherchain = EtherchainOrg(10, 600)

    while True:
        safe_low_price = etherchain.safe_low_price()
        logging.info(safe_low_price)

        standard_price = etherchain.standard_price()
        logging.info(standard_price)

        fast_price = etherchain.fast_price()
        logging.info(fast_price)

        if safe_low_price is not None and standard_price is not None and fast_price is not None:
            break

        time.sleep(1)

@pytest.mark.timeout(45)
@pytest.mark.skip
def test_metamask_integration():
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)

    metamask = Metamask(10, 600)

    while True:
        safe_low_price = metamask.safe_low_price()
        logging.info(safe_low_price)

        standard_price = metamask.standard_price()
        logging.info(standard_price)

        fast_price = metamask.fast_price()
        logging.info(fast_price)

        if safe_low_price is not None and standard_price is not None and fast_price is not None:
            break

        time.sleep(1)

@pytest.mark.timeout(45)
def test_ethgasstation_integration():
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)

    egs = EthGasStation(10, 600)

    while True:
        safe_low_price = egs.safe_low_price()
        logging.info(safe_low_price)

        standard_price = egs.standard_price()
        logging.info(standard_price)

        fast_price = egs.fast_price()
        logging.info(fast_price)

        if safe_low_price is not None and standard_price is not None and fast_price is not None:
            break

        time.sleep(1)

def test_ethgasstation_url():
    egs = EthGasStation(10, 600)
    assert egs.URL == "https://ethgasstation.info/json/ethgasAPI.json"

    egs = EthGasStation(10, 600, "abcdefg")
    assert egs.URL == "https://ethgasstation.info/json/ethgasAPI.json?api-key=abcdefg"


@pytest.mark.timeout(45)
def test_etherscan_integration():
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)

    etherscan = Etherscan(10, 600)

    while True:
        safe_low_price = etherscan.safe_low_price()
        logging.info(safe_low_price)

        standard_price = etherscan.standard_price()
        logging.info(standard_price)

        fast_price = etherscan.fast_price()
        logging.info(fast_price)

        if safe_low_price is not None and standard_price is not None and fast_price is not None:
            break

        time.sleep(10)

@pytest.mark.timeout(45)
def test_polygonscan_integration():
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)

    polygonscan = Polygonscan(10, 600)

    while True:
        safe_low_price = polygonscan.safe_low_price()
        logging.info(safe_low_price)

        standard_price = polygonscan.standard_price()
        logging.info(standard_price)

        fast_price = polygonscan.fast_price()
        logging.info(fast_price)

        fast_price = polygonscan.fast_price()
        logging.info(fast_price)

        suggest_base_fee = polygonscan._suggest_base_fee
        logging.info(suggest_base_fee)

        if safe_low_price is not None and standard_price is not None and fast_price is not None and suggest_base_fee is not None:
            break

        time.sleep(10)

def test_polygonscan_url():
    polygonscan = Polygonscan(10, 600)
    assert polygonscan.URL == "https://api.polygonscan.com/api?module=gastracker&action=gasoracle"

    polygonscan = Polygonscan(10, 600, "abcdefg")
    assert polygonscan.URL == "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=abcdefg"

def test_etherscan_url():
    etherscan = Etherscan(10, 600)
    assert etherscan.URL == "https://api.etherscan.io/api?module=gastracker&action=gasoracle"

    etherscan = Etherscan(10, 600, "abcdefg")
    assert etherscan.URL == "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=abcdefg"

@pytest.mark.timeout(45)
@pytest.mark.skip
def test_gasnow_integration():
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)

    gasnow = GasNow(10, 600, "MyTestApp456")

    while True:
        safe_low_price = gasnow.safe_low_price()
        logging.info(safe_low_price)

        standard_price = gasnow.standard_price()
        logging.info(standard_price)

        fast_price = gasnow.fast_price()
        logging.info(fast_price)

        fastest_price = gasnow.fastest_price()
        logging.info(fast_price)

        if safe_low_price is not None and standard_price is not None and fast_price is not None and fastest_price is not None:
            break

        time.sleep(10)

@pytest.mark.skip
def test_gasnow_url():
    gasnow = GasNow(10, 600)
    assert gasnow.URL == "https://www.gasnow.org/api/v3/gas/price"

    gasnow = GasNow(10, 600, "abcdefg")
    assert gasnow.URL == "https://www.gasnow.org/api/v3/gas/price?utm_source=abcdefg"

@pytest.mark.timeout(45)
@pytest.mark.skip
def test_ethgaswatch_integration():
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)

    gasnow = EthGasWatch(10, 600)

    while True:
        safe_low_price = gasnow.safe_low_price()
        logging.info(safe_low_price)

        standard_price = gasnow.standard_price()
        logging.info(standard_price)

        fast_price = gasnow.fast_price()
        logging.info(fast_price)

        fastest_price = gasnow.fastest_price()
        logging.info(fast_price)

        if safe_low_price is not None and standard_price is not None and fast_price is not None and fastest_price is not None:
            break

        time.sleep(10)
