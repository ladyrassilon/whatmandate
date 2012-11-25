from django.db import models

# Create your models here.

ELECTION_TYPES = (
	('B',"By-Election"),
	('G',"General Election"),
)

class Election(models.Model):
	title = models.CharField(max_length=100,unique=True)
	date = models.DateField(blank=True,null=True)
	kind = models.CharField(max_length=1,choices=ELECTION_TYPES,default="G")

class Region(models.Model):
	name = models.CharField(max_length=100,unique=True)

class Constituency(models.Model):
	name = models.CharField(max_length=100,unique=True)
	region = models.ForeignKey(Region)

class PoliticalParty(models.Model):
	name = models.CharField(max_length=100,unique=True)

class Candidate(models.Model):
	name = models.CharField(max_length=200)
	party = models.ForeignKey(PoliticalParty)
	#slight hack as far as uniqueness for data over time/space is concerned
	constituency_id = models.CharField(max_length=100)

class ConstituencyElection(models.Model):
	election = models.ForeignKey(Election)
	constituency = models.ForeignKey(Constituency)
	electorate_size = models.IntegerField()

class CandidateResult(models.Model):
	candidate = models.ForeignKey(Candidate)
	constituency_election = models.ForeignKey(ConstituencyElection)
	votes = models.IntegerField()

