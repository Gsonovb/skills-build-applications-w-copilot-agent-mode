from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # 连接到 MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # 删除现有的集合
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        
        self.stdout.write(self.style.SUCCESS('Dropped existing collections. Creating new test data...'))

        # 创建用户
        users = [
            User(_id=ObjectId(), username='eaglestar', email='eaglestar@mschool.edu', password='eaglestarpassword'),
            User(_id=ObjectId(), username='swiftcode', email='swiftcode@mschool.edu', password='swiftcodepassword'),
            User(_id=ObjectId(), username='octoprime', email='octoprime@mschool.edu', password='octoprimepassword'),
            User(_id=ObjectId(), username='marinediver', email='marinediver@mschool.edu', password='marinediverpassword'),
            User(_id=ObjectId(), username='codehawk', email='codehawk@mschool.edu', password='codehawkpassword'),
        ]
        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS('Created {} users'.format(len(users))))

        # 创建团队
        blue_team = Team(_id=ObjectId(), name='Blue Team')
        blue_team.save()
        gold_team = Team(_id=ObjectId(), name='Gold Team')
        gold_team.save()
        
        # 将用户添加到团队
        blue_team.members.add(users[0], users[2], users[4])
        gold_team.members.add(users[1], users[3])
        self.stdout.write(self.style.SUCCESS('Created teams and added members'))

        # 创建活动
        activities = [
            Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
            Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
            Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
            Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
            Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
        ]
        Activity.objects.bulk_create(activities)
        self.stdout.write(self.style.SUCCESS('Created {} activities'.format(len(activities))))

        # 创建排行榜条目
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user=users[0], score=100),
            Leaderboard(_id=ObjectId(), user=users[1], score=90),
            Leaderboard(_id=ObjectId(), user=users[2], score=95),
            Leaderboard(_id=ObjectId(), user=users[3], score=85),
            Leaderboard(_id=ObjectId(), user=users[4], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)
        self.stdout.write(self.style.SUCCESS('Created {} leaderboard entries'.format(len(leaderboard_entries))))

        # 创建锻炼计划
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)
        self.stdout.write(self.style.SUCCESS('Created {} workouts'.format(len(workouts))))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))