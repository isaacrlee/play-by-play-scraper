from django.db import models

# Create your models here.


class Team (models.Model):
    tbc_team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    conference = models.CharField(max_length=50)


class Player(models.Model):
    L = 'LEFT'
    S = 'SWITCH'
    R = 'RIGHT'
    HANDEDNESS_CHOICES = (
        (L, 'Left'),
        (S, 'Switch'),
        (R, 'Right'),
    )
    tbc_player_id = models.IntegerField(primary_key=True)
    pitcher_handedness = models.CharField(
        max_length=1, choices=HANDEDNESS_CHOICES)
    batter_handedness = models.CharField(
        max_length=1, choices=HANDEDNESS_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Game (models.Model):
    date = models.DateTimeField()
    home_team = models.ForeignKey(
        Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(
        Team, related_name='away_team', on_delete=models.CASCADE)


class Play (models.Model):
    SINGLE = '1B'
    DOUBLE = '2B'
    TRIPLE = '3B'
    HOMERUN = 'HR'
    GROUNDOUT = 'G'
    LINEOUT = 'L'
    FLYOUT = 'F'
    ERROR = 'E'
    STRIKEOUT = 'K'
    WALK = 'BB'
    HITBYPITCH = 'HBP'

    PITCHER = 'P'
    FIRSTBASE = '1B'
    SECONDBASE = '2B'
    THIRDBASE = '3B'
    SHORTSTOP = 'SS'
    LEFTFIELD = 'LF'
    CENTERFIELD = 'CF'
    RIGHTFIELD = 'RF'
    LEFTCENTER = 'LC'
    RIGHTCENTER = 'RC'
    LEFTSIDE = 'LS'
    MIDDLE = 'M'
    RIGHTSIDE = 'RS'

    RESULT_CHOICES = (
        (SINGLE, 'Single'),
        (DOUBLE, 'Double'),
        (TRIPLE, 'Triple'),
        (HOMERUN, 'Home Run'),
        (GROUNDOUT, 'Ground Out'),
        (LINEOUT, 'Line Out'),
        (FLYOUT, 'Fly Out'),
        (ERROR, 'Error'),
        (STRIKEOUT, 'Strike Out'),
        (WALK, 'Walk'),
        (HITBYPITCH, 'Hit By Pitch'),
    )

    LOCATION_CHOICES = (
        (PITCHER, 'Pitcher'),
        (FIRSTBASE, 'First Base'),
        (SECONDBASE, 'Second Base'),
        (THIRDBASE, 'Third Base'),
        (SHORTSTOP, 'Shortstop'),
        (LEFTFIELD, 'Left Field'),
        (CENTERFIELD, 'Center Field'),
        (RIGHTFIELD, 'Right Field'),
        (LEFTCENTER, 'Left Center'),
        (RIGHTCENTER, 'Right Center'),
        (LEFTSIDE, 'Left Side'),
        (MIDDLE, 'Middle'),
        (RIGHTSIDE, 'Right Side'),
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    play_text = models.CharField(max_length=200)
    offense_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pitcher = models.ForeignKey(Player, on_delete=models.CASCADE)
    pa_result = models.CharField(max_length=3, choices=RESULT_CHOICES)
    batted_ball_location = models.CharField(
        max_length=2, choices=LOCATION_CHOICES)
