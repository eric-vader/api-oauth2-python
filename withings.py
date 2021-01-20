from withings_api import WithingsAuth, WithingsApi, AuthScope
from withings_api.common import get_measure_value, MeasureType, NotifyAppli
from enum import Enum, IntEnum

auth = WithingsAuth(
    client_id='bd7fa1e13e826e59cf239e309f53b765b706e90bdcd4e7f87f9b6378481605af',
    consumer_secret='1739c24a9971681ea82abc4b10a44882584eeaf6334eaebdbfd54df7396270fc',
    callback_uri='https://asia-southeast2-eric-han.cloudfunctions.net/nus-withings-bridge',
    scope=(
        AuthScope.USER_ACTIVITY,
        AuthScope.USER_METRICS,
        AuthScope.USER_INFO,
        AuthScope.USER_SLEEP_EVENTS,
    )
)

authorize_url = auth.get_authorize_url()
# Have the user goto authorize_url and authorize the app. They will be redirected back to your redirect_uri.
print(authorize_url)

code = input("Enter Code: ")
credentials = auth.get_credentials(code)

# Now you are ready to make calls for data.
api = WithingsApi(credentials)

ll = api.notify_list()
print(ll)



api.notify_subscribe(
    callbackurl="https://asia-southeast2-eric-han.cloudfunctions.net/nus-withings-bridge",
    appli=NotifyAppli.WEIGHT,
    comment="Sync to NUS Temp Taking HTD",
)
'''

meas_result = api.measure_get_meas()

for measure_type in [MeasureType.BODY_TEMPERATURE]:
    m = get_measure_value(meas_result, with_measure_type=measure_type)
    print(m)

#?code=aa7edaf72e562619dfd31aa6f2f4a6b20a3fa089&state=7vSdgJ3jXTeEiL9KRMWSgWBQHUzqyo
'''