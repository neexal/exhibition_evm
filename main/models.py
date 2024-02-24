from django.db import models

class Stall(models.Model):
    stall_number = models.IntegerField(unique=True)
    total_votes = models.IntegerField(default=0)
    
    # def __str__(self):
    #     return self.stall_number
    

class Voter(models.Model):
    voting_id = models.CharField(max_length=100, unique=True)
    selected_stalls = models.ManyToManyField(Stall)

    def __str__(self):
        return self.voting_id