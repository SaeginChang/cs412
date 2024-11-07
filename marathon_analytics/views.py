from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import *
from .models import Result

import plotly
import plotly.graph_objects as go

# Create your views here.

class ResultsListView(ListView):
    '''View to show a list of result.'''

    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'result'

    def get_queryset(self) -> QuerySet[Any]:
        '''return the set of Results'''

        # use the superclass version of the queryset
        qs = super().get_queryset()
        # return qs[:25] # return 25 records for now

        # if we have a search paramter, use it to filter the query set
        if 'city' in self.request.GET:
            
            city = self.request.GET['city']
            if city: # not empty string:
                qs = Result.objects.filter(city__icontains=city)

        return qs
    
class ResultDetailView(DetailView):
    '''Dispay a single Result on it's own page'''

    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'

    # implement some methods...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        r = context['r'] # obtain the single Result Instance

        # get data: half-marathon splits
        first_half_seconds = (r.time_half1.hour * 3600 +
                               r.time_half1.minute * 60 + 
                               r.time_half1.second)
        
        second_half_seconds = (r.time_half2.hour * 3600 +
                               r.time_half2.minute * 60 + 
                               r.time_half2.second)

        # build a pie chart
        x = ['first half time', 'second half time']
        y = [first_half_seconds, second_half_seconds]
        # print(f'x={x}')
        # print(f'y={y}')
        fig = go.Pie(labels=x, values=y)
        pie_div = plotly.offline.plot({'data':[fig]},
                                      auto_open=False,
                                      output_type='div'
                                      )

        # add the pie chart to the context
        context['pie_div'] = pie_div

        return context
    
