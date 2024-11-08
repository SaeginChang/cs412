from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import *
from .models import Voter
from django.db.models import *
from django.utils import timezone
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        # Filtering logic here as before
        queryset = super().get_queryset()
        # Add your filtering code here as needed
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print("voterListView context data loaded")
        current_year = timezone.now().year
        context['years'] = list(range(1900, current_year + 1))  # List of years for date filtering
        context['voter_scores'] = list(range(6))  # List of voter scores (0-5)
        return context

    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        # Apply filters if any are selected in the form
        queryset = super().get_queryset()
        party_affiliation = self.request.GET.get('party_affiliation')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        # Apply filtering logic
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_birth_year)
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_birth_year)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Year of Birth Histogram
        birth_years = queryset.values_list('date_of_birth__year', flat=True)
        birth_year_histogram = px.histogram(
            x=birth_years,
            title="Distribution of Voters by Year of Birth",
            labels={'x': 'Year of Birth', 'y': 'Count'},
        )
        birth_year_histogram_div = plot(birth_year_histogram, output_type='div')

        # Party Affiliation Pie Chart
        party_counts = queryset.values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_pie = px.pie(
            names=[party['party_affiliation'] for party in party_counts],
            values=[party['count'] for party in party_counts],
            title="Distribution of Voters by Party Affiliation"
        )
        party_pie_div = plot(party_pie, output_type='div')

        # Election Participation Histogram
        election_data = {
            '2020 State': queryset.filter(v20state=True).count(),
            '2021 Town': queryset.filter(v21town=True).count(),
            '2021 Primary': queryset.filter(v21primary=True).count(),
            '2022 General': queryset.filter(v22general=True).count(),
            '2023 Town': queryset.filter(v23town=True).count(),
        }
        election_participation_histogram = go.Figure(
            data=[go.Bar(x=list(election_data.keys()), y=list(election_data.values()))],
            layout_title_text="Distribution of Voters by Election Participation"
        )
        election_participation_histogram_div = plot(election_participation_histogram, output_type='div')

        # Add graphs to context
        context['birth_year_histogram_div'] = birth_year_histogram_div
        context['party_pie_div'] = party_pie_div
        context['election_participation_histogram_div'] = election_participation_histogram_div

        # Years for dropdown in the filter form
        current_year = timezone.now().year
        context['years'] = list(range(1900, current_year + 1))
        context['voter_scores'] = list(range(6))  # Voter scores (0-5)
        
        return context