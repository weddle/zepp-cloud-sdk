# References and Prior Work Consulted

This file credits external projects, articles, and documentation that informed our research, probing, and scripts. Links point to the original sources; notes summarize what we took from each.


## Community Repositories

- micw/hacking-mifit-api: GitHub repository documenting Mi Fit API usage
  - Link: https://github.com/micw/hacking-mifit-api
  - Informed: use of `GET /v1/data/band_data.json` with `apptoken` and `userid`, Base64-encoded daily summaries containing sleep and steps.


- H3llK33p3r/zepp-fit-extractor: Java client for Zepp webservices
  - Link: https://github.com/H3llK33p3r/zepp-fit-extractor
  - Informed: header pattern (`apptoken`, `appPlatform: web`, `appname: com.xiaomi.hm.health`), workout endpoints (`/v1/sport/run/history.json`, `/v1/sport/run/detail.json`) and pagination.


- rolandsz/Mi-Fit-and-Zepp-workout-exporter: scripts to export workouts
  - Link: https://github.com/rolandsz/Mi-Fit-and-Zepp-workout-exporter
  - Informed: confirmation of workout endpoints and header patterns similar to zepp-fit-extractor.



## Articles and Blog Posts

- Roland Szabo: Export Mi Fit and Zepp workout data
  - Link: https://rolandszabo.com/posts/export-mi-fit-and-zepp-workout-data/
  - Informed: practical patterns for exporting workouts, reinforcing endpoint and header usage.


- BTasker Projects: Zepp to InfluxDB (heart-rate data format wiki)
  - Link: https://projects.bentasker.co.uk/gils_projects/wiki/utilities/zepp_to_influxdb/page/Heart-Rate-Data-Format.html
  - Informed: structure and encoding of heart-rate related payloads; our `data_hr` decoder follows the documented per‑minute byte format (1440 bytes; 254/255 invalid, 0 invalid).


- BTasker Blog: Writing data from a Bip 3 Smartwatch into InfluxDB
  - Link: https://www.bentasker.co.uk/posts/blog/software-development/extracting-data-from-zepp-app-for-local-storage-in-influxdb.html
  - Informed: confirmation of API surfaces and event types exposed via cloud endpoints.


- BTasker Issues: Zepp to InfluxDB probes (stress, SpO2, PAI, menstrual)
  - Stress (#1): https://projects.bentasker.co.uk/gils_projects/issue/utilities/zepp_to_influxdb/1.html
  - SpO2 (#2): https://projects.bentasker.co.uk/gils_projects/issue/utilities/zepp_to_influxdb/2.html
  - PAI (#7): https://projects.bentasker.co.uk/gils_projects/issue/utilities/zepp_to_influxdb/7.html
  - Informed: expected `eventType` names and envelope shapes for `/users/<uid>/events`.



## Official and Community Documentation

- Zepp OS Developers: checkSystemApp
  - Link: https://docs.zepp.com/docs/reference/device-app-api/newAPI/router/checkSystemApp/
  - Informed: taxonomy of “system apps” (Sleep, SpO2, Stress, Thermometer, Body Composition, Readiness) to derive candidate `eventType` names.


- Zepp OS Developers: hmUI data_type
  - Link: https://docs.zepp.com/docs/watchface/api/hmUI/widget/data_type/
  - Informed: naming conventions and signals that guided candidate probes.


- Gadgetbridge: Zepp OS basics/features
  - Link: https://gadgetbridge.org/basics/topics/zeppos/
  - Informed: features surfaced by devices (HRV, sleep respiratory rate, temperature) that map to plausible cloud event names.


- Amazfit/Zepp technology and product pages
  - Amazfit technology page: https://us.amazfit.com/pages/amazfit-technology-page-health-technology
  - Zepp technology page: https://www.zepp.com/technology
  - Amazfit Active product page: https://us.amazfit.com/products/amazfit-active
  - Informed: product‑level features and terminology used to hypothesize event types and metrics.


- Device manuals
  - Amazfit Balance user manual (PDF): https://manual-cdn.zepp.com/uploads/doc/20230901/169353352980.pdf
  - Amazfit Smart Scale manual: https://manuals.plus/amazfit/amazfit-smart-scale-manual
  - Informed: presence of temperature, body composition, and related feature names used to guide probes.


- Huami/Zepp blog
  - Meet the New and Improved Zepp App: https://www.huami.com/blog/meet-the-the-new-improved-zepp-app
  - Informed: naming and categorization that supported probe planning.



## Hostnames and Endpoints (for context)

- Huami API base used: https://api-mifit.huami.com (plus regional variants)
- Zepp events base used: https://api-mifit-us2.zepp.com (plus regional variants)
- OAuth/Account references: https://account.huami.com/



## Notes on Use

- We only used publicly accessible information from the above sources to shape our probes and scripts.
- If any owners of the referenced projects prefer alternative attribution or wish links to be updated, we can adapt this file accordingly.
