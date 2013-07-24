from bullhorn.models import Metadata
from django.http import HttpResponse
import json


def get_metadata(request):

    metadata = Metadata.objects.values_list('display_name', flat=True)
    metadata = {meta: meta for meta in metadata}
    data = json.dumps(metadata)
    return HttpResponse(data, mimetype='application/json')
