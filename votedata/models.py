from django.db import models
import math
import json
from django.core.cache import cache
from django.core.urlresolvers import reverse

# Create your models here.

CACHE_SECONDS = 60*60*24*365

ELECTION_TYPES = (
	('B',"By-Election"),
	('G',"General Election"),
)

class Election(models.Model):
	title = models.CharField(max_length=100,unique=True)
	date = models.DateField(blank=True,null=True)
	kind = models.CharField(max_length=1,choices=ELECTION_TYPES,default="G")

	def _get_constituency_results(self):
		print "cache fail"
		constituency_results = [{
			"name":result.constituency.name,
			"turnout_percentage":result.turnout_percentage(),
			"winner_total_percentage":result.winner_total_percentage(),
			"abstention_percentage":result.abstention_percentage()} for result in self.constituencyelection_set.all()]
		cache.set("ecr%s"%(self.id),constituency_results,CACHE_SECONDS)
		return constituency_results
	def get_constituency_results(self):
		results = cache.get("ecr%s"%(self.id),False)
		if not results:
			results = self._get_constituency_results()
		return results


	def __unicode__(self):
		return self.title
	def get_absolute_url(self):
		return reverse("election_detail",kwargs={"election_id":self.id})

class Region(models.Model):
	name = models.CharField(max_length=100,unique=True)
	def __unicode__(self):
		return self.name

class Constituency(models.Model):
	name = models.CharField(max_length=100,unique=True)
	region = models.ForeignKey(Region)
	def __unicode__(self):
		return "%s - %s"%(self.region.name,self.name)

class PoliticalParty(models.Model):
	name = models.CharField(max_length=100,unique=True)
	def __unicode__(self):
		return self.name

class Candidate(models.Model):
	name = models.CharField(max_length=200)
	party = models.ForeignKey(PoliticalParty)
	#slight hack as far as uniqueness for data over time/space is concerned
	constituency_id = models.CharField(max_length=100)
	def __unicode__(self):
		return "%s (%s)"%(self.name,self.party.name)

class ConstituencyElection(models.Model):
	election = models.ForeignKey(Election)
	constituency = models.ForeignKey(Constituency)
	electorate_size = models.IntegerField()

	def _calculate_turnout_percentage(self):
		total = 0
		for cr in self.candidateresult_set.all():
			total += cr.votes
		turnout_percentage = round(float(total)/float(self.electorate_size)*100)
		cache.set("constituency_election.turnout_percentage.%s,%s"%(self.election_id,self.constituency_id),turnout_percentage,CACHE_SECONDS)
		return turnout_percentage

	def turnout_percentage(self):
		turnout_percentage = cache.get("constituency_election.turnout_percentage.%s,%s"%(self.election_id,self.constituency_id),False)
		if not turnout_percentage:
			turnout_percentage = self._calculate_turnout_percentage()
		return turnout_percentage
	#FIXME:This needs caching
	def conventional_party_results(self):
		tally = {}
		total = 0
		for cr in self.candidateresult_set.all():
			total += cr.votes
			tally[cr.candidate.party.name] = cr.votes
		results = {}
		results_list = []
		for party in tally.keys():
			results[party] = round((float(tally[party])/float(total))*100,2)
			results_list.append("%s:%d02"%(party,results[party]))
		return results
	#FIXEME:This needs caching
	def winner(self):
		largest_party = None
		largest_total = 0
		for cr in self.candidateresult_set.all():
			if cr.votes > largest_total:
				largest_total = cr.votes
				largest_party = cr.candidate.party.name
		return largest_party

	def _calculate_winner_total_percentage(self):
		largest_party = None
		largest_total = 0
		for cr in self.candidateresult_set.all():
			if cr.votes > largest_total:
				largest_total = cr.votes
				largest_party = cr.candidate.party.name
		winner_total_percentage = round((float(largest_total)/float(self.electorate_size))*100,2)
		cache.set("constituency_election.winner_total_percentage.%s,%s"%(self.election_id,self.constituency_id),winner_total_percentage,CACHE_SECONDS)
		return winner_total_percentage
	def winner_total_percentage(self):
		winner_total_percentage = cache.get("constituency_election.winner_total_percentage.%s,%s"%(self.election_id,self.constituency_id),False)
		if not winner_total_percentage:
			winner_total_percentage = self._calculate_winner_total_percentage()
		return winner_total_percentage

	def _calculate_abstention_percentage(self):
		abstention_percentage = 100 - self.turnout_percentage()
		cache.set("constituency_election.abstention_percentage.%s,%s"%(self.election_id,self.constituency_id),abstention_percentage,CACHE_SECONDS)
		return abstention_percentage
	def abstention_percentage(self):
		abstention_percentage = cache.get("constituency_election.abstention_percentage.%s,%s"%(self.election_id,self.constituency_id),False)
		if not abstention_percentage:
			abstention_percentage = self._calculate_abstention_percentage()
		return abstention_percentage

	def __unicode__(self):
		return "%s (%s)"%(self.constituency.name,self.election.title)

class CandidateResult(models.Model):
	candidate = models.ForeignKey(Candidate)
	constituency_election = models.ForeignKey(ConstituencyElection)
	votes = models.IntegerField()
	def __unicode__(self):
		return "%s (%s,%s)"%(self.candidate.name,self.candidate.party.name,self.constituency_election.election)

