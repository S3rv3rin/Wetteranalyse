
import time
from deutschland import dwd
from deutschland.dwd.api import default_api
from deutschland.dwd.model.station_overview import StationOverview
from deutschland.dwd.model.error import Error
from deutschland.dwd.model.station_overview_extended_get_station_ids_parameter_inner import \
    StationOverviewExtendedGetStationIdsParameterInner
from pprint import pprint
# Defining the host is optional and defaults to https://app-prod-ws.warnwetter.de/v30
# See configuration.py for a list of all supported configuration parameters.
configuration = dwd.Configuration(
    host = "https://app-prod-ws.warnwetter.de/v30"
)


# Enter a context with an instance of the API client
with dwd.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    station_ids = ['10552', '10554', 'Q016', '10514', '10516', '10557', '10558', 'K964']
    # [StationOverviewExtendedGetStationIdsParameterInner] | Beim Parameter stationsIds handelt es sich um die
    # Stationskennungen des DWD. Die Liste der Stationskennungen kann z.B.
    # [hier](https://www.dwd.de/DE/leistungen/klimadatendeutschland/stationsliste.html) eingesehen werden. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Wetterstation Daten
        api_response = api_instance.station_overview_extended_get(station_ids=station_ids)
        pprint(api_response)
    except dwd.ApiException as e:
        print("Exception when calling DefaultApi->station_overview_extended_get: %s\n" % e)
