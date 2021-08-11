[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/docs/faq/custom_repositories)
[![buymeacoffee_badge](https://img.shields.io/badge/Donate-Buy%20Me%20a%20Coffee-ff813f?style=flat)](https://www.buymeacoffee.com/PiotrMachowski)
[![paypalme_badge](https://img.shields.io/badge/Donate-PayPal-0070ba?style=flat)](https://paypal.me/PiMachowski)
![GitHub All Releases](https://img.shields.io/github/downloads/PiotrMachowski/Home-Assistant-custom-components-Froggy/total)

# Froggy Sensor

This custom integration retrieves opening status of [Żabka shops](https://www.zabka.pl/).


![example](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Froggy/blob/master/example.png)

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be added to HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories):
* URL: `https://github.com/PiotrMachowski/Home-Assistant-custom-components-Froggy`
* Category: `Integration`

After adding a custom repository you can use HACS to install this integration using user interface.

### Manual

To install this integration manually you have to download [*froggy.zip*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Froggy/releases/latest/download/froggy.zip) extract its contents to `config/custom_components/froggy` directory:
```bash
mkdir -p custom_components/froggy
cd custom_components/froggy
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-Froggy/releases/latest/download/froggy.zip
unzip froggy.zip
rm froggy.zip
```

## Configuration

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | `string` | `False` | `Froggy` | Prefix for sensor ids |
| `latitude` | `float` | `False` | Latitude of home | Latitude of point of reference |
| `longitude` | `float` | `False` | Longitude of home | Longitude of of reference |
| `shop_ids` | `list` | `False` | - | List of monitored shop ids (ID can be retrieved from [this](https://www.zabka.pl/znajdz-sklep) page) |

### Example configuration

#### Minimal version - retrieves data for the closest shop

```yaml
binary_sensor:
  - platform: froggy
```

#### Selected list of shops
```yaml
binary_sensor:
  - platform: froggy
    shop_ids:
      - ID02786
      - ID07971  
```

### Retrieving shop id
1. Go to [Lokalizator](https://www.zabka.pl/znajdz-sklep)
1. Find the store
1. Double-click on pin
1. Shop id will be visible in URL address:
   
    `https://www.zabka.pl/znajdz-sklep/sklep/ID02786,ustrzyki-dolne-ul-rynek-25-u2`

<a href="https://www.buymeacoffee.com/PiotrMachowski" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
