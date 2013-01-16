#
# TEMPORARY CODE - DUCKSBOARD INTERFACING METRICS
# RECORDING. CURRENTLY RECORDS PUBLICATIONS AND
# TOTAL NUMBER OF PUBLISHED PAGES.
#
# Note that all of this is post-and-forget, so we
# ignore any posting errors that libsaas reports
# during post function calls.
#
from libsaas.services import ducksboard
import time

class Recorder:

    # test API key (tied to mofodev's ducksboard at https://public.ducksboard.com/H_e17YwSCEYBNxfLv5sg)
    apikey = "ntQg43WhJFAAhxgm4dmZj1gFl56cLCg6SMmxNW5a9YUVW1Ca3j"

    # set up the "connetions" for the two widgets
    service = ducksboard.Ducksboard(apikey)

    # label for our specific tracking widgets
    totalPub = service.data_source("totalPub")
    goodPub = service.data_source("goodPub")
    goodPubMonth = service.data_source("goodPubMonth")

    # publication failures
    nobody = service.data_source("nobody")
    nohttp = service.data_source("nohttp")
    toolarge = service.data_source("toolarge")


    # track individual publications over time
    def trackNewPublication(this):
        try:
            this.goodPub.push({'delta': 1, 'timestamp': time.time()})
            this.goodPubMonth.push({'delta': 1, 'timestamp': time.time()})
        except:
            pass

    # track bad publications over time - no content supplied
    def trackBadPublication_noBody(this):
        try:
            this.nobody.push({'delta': 1, 'timestamp': time.time()})
        except:
            pass

    # track bad publications over time - publication wasn't over http/https
    def trackBadPublication_noHTTP(this):
        try:
            this.nohttp.push({'delta': 1, 'timestamp': time.time()})
        except:
            pass

    # track bad publications over time - the page is too big to publish
    def trackBadPublication_tooLarge(this):
        try:
            this.toolarge.push({'delta': 1, 'timestamp': time.time()})
        except:
            pass

    # track database size over time, based on delta recording
    def trackTotalPublications(this):
        try:
            this.totalPub.push({'delta': 1, 'timestamp': time.time()})
        except:
            pass

    # fix database size for some time.
    def setTotalPublications(this, value):
        try:
            this.totalPub.push({'value': value, 'timestamp': time.time()})
        except:
            pass