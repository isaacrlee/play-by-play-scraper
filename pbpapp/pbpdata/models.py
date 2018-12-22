from django.db import models

# Create your models here.


class Team (models.Model):
    # tbc_id
    team_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    conference = models.CharField(max_length=50)


class Player(models.Model):
    HANDEDNESS_CHOICES = (
        ('L', 'Left'),
        ('S' 'Switch'),
        ('R', 'Right')
    )
    pitcher_handedness = models.CharField(
        max_length=1, choices=HANDEDNESS_CHOICES)
    batter_handedness = models.CharField(
        max_length=1, choices=HANDEDNESS_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL)


class Game (models.Model):
    date = models.DateTimeField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Play (models.Model):
    RESULT_CHOICES = (
        ('1B', 'Single'),
        ('2B' 'Double'),
        ('3B', 'Triple'),
        ('HR', 'Home Run'),
        ('G', 'Ground Out'),
        ('L', 'Line Out'),
        ('F', 'Fly Out'),
        ('E', 'Error'),
        ('K', 'Strike Out'),
        ('BB', 'Walk'),
        ('HBP', 'Hit By Pitch')
    )
    LOCATION_CHOICES = (
        ('P', 'Pitcher'),
        ('1B', 'First Base'),
        ('2B', 'Second Base'),
        ('3B', 'Third Base'),
        ('SS', 'Shortstop'),
        ('LF', 'Left Field'),
        ('CF', 'Center Field'),
        ('RF', 'Right Field'),
        ('LC', 'Left Center'),
        ('RC', 'Right Center'),
        ('LS', 'Left Side'),
        ('M', 'Middle'),
        ('RS', 'Right Side')
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    play_text = models.CharField(max_length=200)
    offense_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pitcher = models.ForeignKey(Player, on_delete=models.CASCADE)
    pa_result = models.CharField(max_length=3, choices=RESULT_CHOICES)
    batted_ball_location = models.CharField(
        max_length=2, choices=LOCATION_CHOICES)
