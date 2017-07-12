import os

import requests
from django.db.models import Count
from django.db.models.functions import TruncDay

from requests.auth import HTTPBasicAuth

from klog.models import Log



def getFork(src):
    full_route = 'main/java/com/amerino'
    full_route = full_route.split('/')
    r = requests.get("https://api.bitbucket.org/2.0/repositories/deixona/loggingexample/src/",
                     auth=HTTPBasicAuth(os.environ["BITBUCKET_USER"], os.environ["BITBUCKET_CODE"]))
    araay = r.json()
    next_url = next(x for x in araay.get('values') if x.get('path') == 'src').get('links').get('self').get('href')
    next_path = 'src'
    repoUrl = getRepoUrl(full_route, next_path, next_url)
    return estructura


def getRepoUrl(full_route, next_path, next_url):
    for currentFolder in full_route:
        next_path = next_path + '/' + currentFolder
        r = requests.get(next_url, auth=HTTPBasicAuth(os.environ["BITBUCKET_USER"], os.environ["BITBUCKET_CODE"]))
        araay = r.json()
        next_url = next(x for x in araay.get('values') if x.get('path') == next_path).get('links').get('self').get(
            'href')
    return next_url




if __name__ == "__main__":
    print(Log.objects \
          .annotate(date=TruncDay('date_time')) \
          .values('date') \
          .annotate(count=Count('id')) \
          .values('date', 'count') \
          .order_by('date')
          )
