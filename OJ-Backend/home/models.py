from django.db import models

class problem(models.Model):
    STATEMENT_MAX_LENGTH = 10000
    NAME_MAX_LENGTH = 255
    CODE_MAX_LENGTH = 255
    DIFFICULTY_MAX_LENGTH = 10

    statement = models.TextField()
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    code = models.CharField(max_length=CODE_MAX_LENGTH)
    difficulty = models.CharField(max_length=DIFFICULTY_MAX_LENGTH, null=True, blank=True)

    def __str__(self):
        return self.name
    
