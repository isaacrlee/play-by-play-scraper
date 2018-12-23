from django.db import models

# Create your models here.


class Team (models.Model):
    tbc_team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    conference = models.CharField(max_length=50)

    def __repr__ (self):
        return self.name

    def __str__ (self):
        return self.name




class Player(models.Model):
    L = 'L'
    S = 'S'
    R = 'R'
    U = 'U'
    HANDEDNESS_CHOICES = (
        (L, 'Left'),
        (S, 'Switch'),
        (R, 'Right'),
        (U, 'Unknown')
    )
    tbc_player_id = models.IntegerField(primary_key=True)
    pitcher_handedness = models.CharField(
        max_length=10, choices=HANDEDNESS_CHOICES, null=True)
    batter_handedness = models.CharField(
        max_length=10, choices=HANDEDNESS_CHOICES, null=True)
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
        (HOMERUN, 'HomeRun'),
        (GROUNDOUT, 'GroundOut'),
        (LINEOUT, 'LineOut'),
        (FLYOUT, 'FlyOut'),
        (ERROR, 'Error'),
        (STRIKEOUT, 'StrikeOut'),
        (WALK, 'Walk'),
        (HITBYPITCH, 'HitByPitch'),
    )

    LOCATION_CHOICES = (
        (PITCHER, 'Pitcher'),
        (FIRSTBASE, 'FirstBase'),
        (SECONDBASE, 'SecondBase'),
        (THIRDBASE, 'ThirdBase'),
        (SHORTSTOP, 'Shortstop'),
        (LEFTFIELD, 'LeftField'),
        (CENTERFIELD, 'CenterField'),
        (RIGHTFIELD, 'RightField'),
        (LEFTCENTER, 'LeftCenter'),
        (RIGHTCENTER, 'RightCenter'),
        (LEFTSIDE, 'LeftSide'),
        (MIDDLE, 'Middle'),
        (RIGHTSIDE, 'RightSide'),
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    play_text = models.CharField(max_length=200)
    offense_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pitcher = models.ForeignKey(Player, on_delete=models.CASCADE)
    pa_result = models.CharField(max_length=25, choices=RESULT_CHOICES, null=True)
    batted_ball_location = models.CharField(
        max_length=25, choices=LOCATION_CHOICES, null=True)
