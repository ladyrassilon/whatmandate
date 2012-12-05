# Create your views here.

from django.shortcuts import render_to_response
from votedata.models import *
from django.template import RequestContext
from django.views.decorators.cache import cache_page

def different_elections(request):
	elections = Election.objects.all()
	return render_to_response("elections.html", {"elections":elections}, RequestContext(request))

# @cache_page(60 * 60 * 4)
def election_detail(request,election_id):
	election = Election.objects.get(id=election_id)
	height_pix = 24*election.constituencyelection_set.count() + 300
	return render_to_response("basic.html", {"election":election,"height_pix":height_pix}, RequestContext(request))