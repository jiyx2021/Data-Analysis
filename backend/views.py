from django.http import JsonResponse
from django.views.decorators.http import require_GET
import json
from python.wc import *  # Adjust the import according to your project structure

# Test function, enter wordcloudtest.json on webpage to import a default json
def wordcloud_data_test(request):
    with open('json/wordcloud2.json') as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)

# Actual function, final version site javascript should be hardcoded to call wordcloud.json, which calls this function
@require_GET
def wordcloud_data(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if not start_date or not end_date:
        return JsonResponse({"error": "Missing start_date or end_date"}, status=400)

    # Call your function that generates the word cloud based on the date range
    data = backend_wordcloud_json(start_date, end_date)

    return JsonResponse(data, safe=False)
