import datetime

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.binary_sensor import ENTITY_ID_FORMAT, PLATFORM_SCHEMA, DEVICE_CLASS_OPENING
from homeassistant.const import (ATTR_LATITUDE, ATTR_LONGITUDE, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME)

try:
    from homeassistant.components.binary_sensor import BinarySensorEntity
except ImportError:
    from homeassistant.components.binary_sensor import BinarySensorDevice as BinarySensorEntity
from homeassistant.helpers.entity import async_generate_entity_id

CONF_SHOP_IDS = 'shop_ids'

DEFAULT_NAME = 'Froggy'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_LATITUDE): cv.string,
    vol.Optional(CONF_LONGITUDE): cv.string,
    vol.Optional(CONF_SHOP_IDS, default=[]): cv.ensure_list,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})


def get_nearest_store(latitude, longitude):
    nearest = None
    distance = 100000
    response = requests.get('https://www.zabka.pl/ajax/shop-clusters.json')
    if response.status_code == 200 and response.content.__len__() > 0:
        stores = response.json()
        for store in stores:
            lat_diff = (float(store['lat']) - latitude)
            lng_diff = (float(store['lng']) - longitude)
            diff = lat_diff * lat_diff + lng_diff * lng_diff
            if diff < distance:
                distance = diff
                nearest = store['id']
    return nearest


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    latitude = config.get(CONF_LATITUDE, hass.config.latitude)
    longitude = config.get(CONF_LONGITUDE, hass.config.longitude)
    store_ids = config.get(CONF_SHOP_IDS)
    if len(store_ids) == 0:
        store_ids.append(get_nearest_store(latitude, longitude))
    dev = []
    for store_id in store_ids:
        if store_id is not None:
            uid = '{}_{}'.format(name, store_id)
            entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, uid, hass=hass)
            dev.append(FroggySensor(store_id, entity_id))
    add_entities(dev, True)


class FroggySensor(BinarySensorEntity):
    def __init__(self, store_id, entity_id):
        self.store_id = store_id
        self.data = None
        self.entity_id = entity_id

    @property
    def name(self):
        return 'Żabka ' + self.data['address']

    @property
    def is_on(self):
        if self.data is None:
            return None
        now = datetime.datetime.now()
        nowSeconds = now.hour * 3600 + now.minute * 60 + now.second
        return self.data['openTimeSeconds'] <= nowSeconds <= self.data['closeTimeSeconds']

    @property
    def extra_state_attributes(self):
        output = dict()
        if self.data is not None:
            now = datetime.datetime.now()
            nowSeconds = now.hour * 3600 + now.minute * 60 + now.second
            output['id'] = self.store_id
            output['opening'] = self.data['openTime']
            output['closing'] = self.data['closeTime']
            output['address'] = self.data['address']
            output['minutes_to_closing'] = int((self.data['closeTimeSeconds'] - nowSeconds) / 60)
            if output['minutes_to_closing'] < 0:
                output['minutes_to_closing'] += 1440
            output['minutes_to_opening'] = int((self.data['openTimeSeconds'] - nowSeconds) / 60)
            if output['minutes_to_opening'] < 0:
                output['minutes_to_opening'] += 1440
            output[ATTR_LATITUDE] = self.data['_geoloc']['lat']
            output[ATTR_LONGITUDE] = self.data['_geoloc']['lng']
        return output

    @property
    def icon(self):
        if self.is_on:
            return 'mdi:store'
        return 'mdi:store-remove'

    @property
    def device_class(self):
        return DEVICE_CLASS_OPENING

    def update(self):
        address = 'https://apkykk0pza-dsn.algolia.net/1/indexes/prod_locator_prod_zabka/' + self.store_id \
                  + '?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.22.1&x-algolia-application-id=APKYKK0PZA&x-algolia-api-key=71ca67cda813cec86431992e5e67ede2'
        request = requests.get(address)
        if request.status_code == 200 and request.content.__len__() > 0:
            self.data = request.json()
