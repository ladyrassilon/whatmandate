# Create your views here.

from django.shortcuts import render_to_response
from votedata.models import *
from django.template import RequestContext
from django.views.decorators.cache import cache_page

def different_elections(request):
	elections = Election.objects.all()
	return render_to_response("elections.html",{"elections",elections},RequestContext(request))

@cache_page(60 * 15)
def election_detail(request,election_id):
	election = Election.objects.get(id=election_id)
	return render_to_response("basic.html",{"election":election},RequestContext(request))