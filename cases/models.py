from django.db import models


class Case(models.Model):
    title = models.CharField(max_length=200)

    description = models.TextField()

    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Hard', 'Hard'),
        ]
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    correct_answer = models.CharField(max_length=1)

    points = models.IntegerField(default=10)

    def __str__(self):
        return self.question_text


class CaseAttempt(models.Model):

    player_name = models.CharField(max_length=100)

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    score = models.IntegerField(default=0)

    completed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.player_name} - {self.case.title} - {self.score}"
