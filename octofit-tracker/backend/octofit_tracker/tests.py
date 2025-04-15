from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta

class ModelTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.test_user = User.objects.create(
            _id=ObjectId(),
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        
        # 创建测试团队
        self.test_team = Team.objects.create(
            _id=ObjectId(),
            name="Test Team"
        )
        self.test_team.members.add(self.test_user)
        
        # 创建测试活动
        self.test_activity = Activity.objects.create(
            _id=ObjectId(),
            user=self.test_user,
            activity_type="Running",
            duration=timedelta(hours=1)
        )
        
        # 创建测试排行榜
        self.test_leaderboard = Leaderboard.objects.create(
            _id=ObjectId(),
            user=self.test_user,
            score=100
        )
        
        # 创建测试锻炼计划
        self.test_workout = Workout.objects.create(
            _id=ObjectId(),
            name="Test Workout",
            description="This is a test workout"
        )

    def test_user_model(self):
        """测试用户模型"""
        user = User.objects.get(email="test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "password123")

    def test_team_model(self):
        """测试团队模型"""
        team = Team.objects.get(name="Test Team")
        self.assertEqual(team.members.first().username, "testuser")

    def test_activity_model(self):
        """测试活动模型"""
        activity = Activity.objects.get(activity_type="Running")
        self.assertEqual(activity.user.username, "testuser")
        self.assertEqual(activity.duration, timedelta(hours=1))

    def test_leaderboard_model(self):
        """测试排行榜模型"""
        leaderboard = Leaderboard.objects.get(user=self.test_user)
        self.assertEqual(leaderboard.score, 100)

    def test_workout_model(self):
        """测试锻炼计划模型"""
        workout = Workout.objects.get(name="Test Workout")
        self.assertEqual(workout.description, "This is a test workout")

class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # 创建测试用户
        self.test_user = User.objects.create(
            _id=ObjectId(),
            username="apiuser",
            email="api@example.com",
            password="apipassword"
        )
        
        # 创建测试团队
        self.test_team = Team.objects.create(
            _id=ObjectId(),
            name="API Team"
        )
        self.test_team.members.add(self.test_user)

    def test_api_root(self):
        """测试 API 根端点"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_user_list(self):
        """测试用户列表端点"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_team_list(self):
        """测试团队列表端点"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_empty_activities(self):
        """测试空活动列表端点"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_empty_leaderboard(self):
        """测试空排行榜列表端点"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_empty_workouts(self):
        """测试空锻炼计划列表端点"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)