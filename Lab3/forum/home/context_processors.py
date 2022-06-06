from .models import Tred


def search(request):
    treds = Tred.objects.all()
    search_context = {}
    treds_set = set()
    if 'search' in request.GET:
        query = request.GET.get('q')
        #filter treds
        filtered_title = treds.filter(title__icontains=query)
        filtered_content = treds.filter(content__icontains=query)
        for element in filtered_title:
            treds_set.add(element)

        for element in filtered_content:
            treds_set.add(element)

        search_context.update({
            'treds': treds_set,
            'query': query
        })
    return search_context
