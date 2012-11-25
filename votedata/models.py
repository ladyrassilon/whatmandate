from django.db import models

# Create your models here.

ELECTION_TYPES = (
	('B',"By-Election"),
	('G',"General Election"),
)

class Election(models.Model):
	title = models.CharField(max_length=100)
	date = models.DateField()
	kind = models.CharField(max_length=1,choices=ELECTION_TYPES)

class Region(models.Model):
	name = models.CharField(max_length=100)

class Constituency(models.Model):
	name = models.CharField(max_length=100)

class ConstituencyElection(models.Model):
	election = models.ForeignKey(Election)
	constituency = models.ForeignKey(Constituency)
	electorate_size = models.IntegerField()

class CandidateResult(models.Model):
	candidate = models.ForeignKey(Candidate)
	votes = models.IntegerField()

class Candidate(models.Model):
	name = models.CharField(max_length=200)
	party = models.ForeignKey(PoliticalParty)

class PoliticalParty(models.Model):
	name = models.CharField(max_length=100)
