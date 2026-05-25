# Markies-besturing (weergestuurd)

Automatische markies-besturing op basis van het Meteotemplate-weerstation, met een
Home Assistant control-dashboard: instelbare drempels en wachttijden via sliders,
drempellijnen in de grafieken, en een statuskaart die laat zien waarom de markiezen
wel of niet bewegen.

Werkt samen met de Meteotemplate-integratie uit deze repo (sensors
`sensor.meteo_waskolkweg_*`). Pas die prefix aan als jouw station anders heet.

## Gedrag

- **Uitvallen (schaduw)** bij felle, warme zon — droog en windstil — na een wachttijd.
- **Intrekken** zodra de straling onder de intrek-drempel zakt of de zon onder is,
  na een wachttijd.
- **Veiligheid**: bij wind boven de drempel of bij regen klappen de markiezen direct
  in. Dit heeft altijd voorrang.
- Reageert ook **na een herstart** en zodra je **automatisch** aanzet (zet meteen de
  juiste stand, zonder op een overgang te wachten).

## Richting / bedrading (BELANGRIJK)

Deze opstelling gebruikt Shelly (Gen4) in cover-modus met een tussenrelais. De fysieke
cover meldt zich omgekeerd. Geverifieerd via hardware-test:

| Service op `cover.rolluik_1/2` (fysiek) | Effect          |
|-----------------------------------------|-----------------|
| `cover.open_cover`                      | INKLAPPEN       |
| `cover.close_cover`                     | UITKLAPPEN      |

De template-covers `cover.markies_1/2` draaien dit om naar intuïtief
(`device_class: awning`): **open = uitgeklapt**, en hun `open_cover` = uitklappen,
`close_cover` = inklappen. Het **dashboard** gebruikt `cover.markies_*`; de
**automatisering** stuurt de fysieke `cover.rolluik_*` rechtstreeks aan met de richting
uit bovenstaande tabel.

> Gaan jouw markiezen de verkeerde kant op? Wissel dan in `automations/markies.yaml`
> alle `cover.open_cover` <-> `cover.close_cover` om, en in `template-covers.yaml`
> idem. Test met de drempels laag en wachttijd 0.

## Installatie

1. **Helpers** — neem `configuration/helpers.yaml` over in je `configuration.yaml`
   (input_boolean + input_number). Herlaad via Ontwikkelhulpmiddelen -> YAML.
2. **Template-sensors** — `configuration/template-sensors.yaml` onder `template:`.
3. **Template-covers** — `configuration/template-covers.yaml` onder `cover:`.
   Herstart Home Assistant zodat de covers en sensors laden.
4. **Automatisering** — `automations/markies.yaml` toevoegen aan `automations.yaml`,
   of via de UI (nieuwe automatisering -> Bewerken in YAML -> plakken).
5. **Dashboards** — `dashboards/markies-control.yaml` en `dashboards/weerstation.yaml`
   elk in een nieuw dashboard plakken (Onbewerkte configuratie-editor).
   Beide vereisen de custom card **apexcharts-card** (HACS -> Frontend).

## Tip: alles in één package

Je kunt helpers + template-sensors + template-covers + automatisering ook samenvoegen
tot één bestand in `config/packages/markies.yaml` (vereist eenmalig
`homeassistant: packages: !include_dir_named packages` in `configuration.yaml`).
Verwijder dan de losse blokken uit `configuration.yaml` om dubbele entities te
voorkomen. Vraag dit gerust na als je het wilt omzetten.

## Entities (overzicht)

Helpers: `input_boolean.markies_auto`, `input_number.markies_zon_drempel`,
`markies_temp_drempel`, `markies_wind_drempel`, `markies_intrek_drempel`,
`markies_uitval_wachttijd`, `markies_intrek_wachttijd`, `markies_regen_wachttijd`.

Sensors: `binary_sensor.markies_mag_uitvallen`, `binary_sensor.markies_mag_intrekken`.

Covers: fysiek `cover.rolluik_1/2`, weergave `cover.markies_1/2`.
