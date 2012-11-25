# Create your views here.

from django.shortcuts import render_to_response
from votedata.models import *
from django.template import RequestContext

def basic_view(request):
	election = Election.objects.get(title="General Election 2010")
	return render_to_response("basic.html",{"election":election},RequestContext(request))