# Meteotemplate Weather Station — Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://hacs.xyz)
[![Validate](https://github.com/sysmx/MeteoTemplate/actions/workflows/validate.yaml/badge.svg)](https://github.com/sysmx/MeteoTemplate/actions/workflows/validate.yaml)
[![Release](https://img.shields.io/github/v/release/sysmx/MeteoTemplate?style=flat-square)](https://github.com/sysmx/MeteoTemplate/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

Custom Home Assistant integratie die data van een
[Meteotemplate](https://www.meteotemplate.com/)-weerstation binnenhaalt als
getypeerde sensors (wind, zon/UV, regen, temperatuur, bodemvocht, …) — inclusief
een kant-en-klaar Lovelace-dashboard en een blueprint voor automatische
zonwering-aansturing.

## Inhoud

- **Integratie** met UI-configuratie (config flow) — geen YAML nodig
- **Sensors** met juiste `device_class`, `unit_of_measurement` en
  `state_class` zodat ze direct werken in dashboards, statistieken en
  energiekaarten
- **Lovelace-dashboard** in `lovelace/weer-dashboard.yaml`
- **Blueprint** voor automatische zonwering in
  `blueprints/automation/meteotemplate/zonwering.yaml`

## Installatie (HACS — aanbevolen)

1. Open HACS → **Integrations** → menu rechtsboven → **Custom repositories**.
2. Voeg toe:
   - Repository: `https://github.com/sysmx/MeteoTemplate`
   - Category: **Integration**
3. Installeer **Meteotemplate Weather Station**.
4. Herstart Home Assistant.
5. Voeg de integratie toe via de knop hieronder:

   [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=meteotemplate)

   (of: **Instellingen → Apparaten & services → Integratie toevoegen →
   Meteotemplate Weather Station**)

## Installatie (handmatig)

1. Kopieer `custom_components/meteotemplate/` naar je Home Assistant
   `config/custom_components/`-map.
2. Herstart Home Assistant.
3. Voeg de integratie toe via de UI (zie knop hierboven).

## Configuratie

Bij het toevoegen van de integratie vraagt Home Assistant om:

- **Host / URL** van je Meteotemplate-installatie (bijv.
  `https://weer.voorbeeld.nl`)
- **API key** (indien jouw template die vereist)
- **Update-interval** in seconden

Daarna verschijnen alle sensors automatisch onder het aangemaakte device.

## Dashboard

Het meegeleverde dashboard staat in
[`lovelace/weer-dashboard.yaml`](lovelace/weer-dashboard.yaml). Toevoegen:

1. **Instellingen → Dashboards → Voeg dashboard toe → Nieuw dashboard in YAML**.
2. Plak de inhoud van het bestand en pas de `entity:`-verwijzingen aan naar
   jouw entity_ids als die afwijken.

## Blueprint: automatische zonwering

[![Open your Home Assistant instance and import a blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fsysmx%2FMeteoTemplate%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fmeteotemplate%2Fzonwering.yaml)

De blueprint
[`blueprints/automation/meteotemplate/zonwering.yaml`](blueprints/automation/meteotemplate/zonwering.yaml)
rolt je zonwering automatisch **uit** bij felle én warme zon (droog en
windstil) en trekt 'm **in** bij te harde windstoten, regen of als de zon weg
is. Wind/regen reageren direct (veiligheid eerst); uitrollen heeft een
instelbare wachttijd zodat een kort zonnetje niet meteen alles uitrolt.

> **Let op:** de blueprint gaat uit van `cover.open = uitrollen/zakken` en
> `cover.close = intrekken/omhoog`. Werkt jouw motor andersom, kies dan een
> cover-entity waarvoor dit klopt of pas de automation na het aanmaken aan.

## Ondersteuning

- Issues / feature requests: [GitHub Issues](https://github.com/sysmx/MeteoTemplate/issues)
- Documentatie Meteotemplate zelf: <https://www.meteotemplate.com/>

## Licentie

[MIT](LICENSE) — © 2026 Michael Lutz
