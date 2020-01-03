from django.contrib.auth.models import User
from django.db import models


class Answer(models.Model):
    answer = models.CharField(max_length=128)
    image_url = models.URLField(null=True, blank=True)
    question = models.ForeignKey('wrestleleague.MatchQuestion', on_delete=models.CASCADE,
                                 related_name='answers',)

    def __str__(self):
        return f"Answer #{self.id} {self.answer} for {self.question}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('wrestleleague.MatchQuestion', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.CharField(max_length=128, null=True, blank=True)
    rationale = models.TextField(null=True, blank=True)
    points_awarded = models.FloatField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def is_correct(self):
        return self.answer == self.question.correct_answer

    def __str__(self):
        return f'Vote {self.user} for {self.question}'


class MatchQuestion(models.Model):
    question = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    correct_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL,
                                       null=True, blank=True)
    event = models.ForeignKey('wrestleleague.Event', on_delete=models.CASCADE,
                              related_name="match_questions")
    text_answer = models.CharField(max_length=255, null=True, blank=True,
                                   help_text="Correct answer for fill in the blank.")
    points = models.FloatField(default=1, help_text="How many points is this worth?")

    def __str__(self):
        return f"{self.question} ({self.event})"


class Event(models.Model):
    title = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    datetime = models.DateTimeField(null=True)
    vote_open = models.DateTimeField(null=True)
    vote_closed = models.DateTimeField(null=True)
    season = models.ForeignKey('wrestleleague.Season', on_delete=models.SET_NULL,
                               null=True, blank=True)
    promotion = models.ForeignKey('wrestleleague.Promotion', on_delete=models.CASCADE,
                                  null=True, blank=True)
    open_for = models.ManyToManyField(User, blank=True,
                                      help_text='Override open and close times for specific users')
    finalized_log = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title} [{self.promotion or 'None'}]"


class Promotion(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Season(models.Model):
    name = models.CharField(max_length=255)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name
