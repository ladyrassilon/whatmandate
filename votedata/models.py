from django.db import models
import math
import json
from django.core.cache import cache
# Create your models here.

ELECTION_TYPES = (
	('B',"By-Election"),
	('G',"General Election"),
)

class Election(models.Model):
	title = models.CharField(max_length=100,unique=True)
	date = models.DateField(blank=True,null=True)
	kind = models.CharField(max_length=1,choices=ELECTION_TYPES,default="G")

	def __unicode__(self):
		return self.title

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
	def turnout_percentage(self):
		total = 0
		for cr in self.candidateresult_set.all():
			total += cr.votes
		return round(float(total)/float(self.electorate_size)*100)
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
	def winner(self):
		largest_party = None
		largest_total = 0
		for cr in self.candidateresult_set.all():
			if cr.votes > largest_total:
				largest_total = cr.votes
				largest_party = cr.candidate.party.name
		return largest_party

	def winner_total_percentage(self):
		largest_party = None
		largest_total = 0
		for cr in self.candidateresult_set.all():
			if cr.votes > largest_total:
				largest_total = cr.votes
				largest_party = cr.candidate.party.name

		return round((float(largest_total)/float(self.electorate_size))*100,2)

	def abstention_percentage(self):
		absentions = self.electorate_size
		for cr in self.candidateresult_set.all():
			absentions -= cr.votes
		return round(float(absentions)/float(self.electorate_size)*100)

	def __unicode__(self):
		return "%s (%s)"%(self.constituency.name,self.election.title)

class CandidateResult(models.Model):
	candidate = models.ForeignKey(Candidate)
	constituency_election = models.ForeignKey(ConstituencyElection)
	votes = models.IntegerField()
	def __unicode__(self):
		return "%s (%s,%s)"%(self.candidate.name,self.candidate.party.name,self.constituency_election.election)

