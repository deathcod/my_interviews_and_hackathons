from .models import info
from rest_framework import serializers

class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = info
		fields = [
		'name',
		'email',
		'mobile',
		'dob',
		'location'
		]

class PostListSerializer(serializers.ModelSerializer):
	class Meta:
		model = info
		fields = [
		'id',
		'name',
		'email',
		'mobile',
		'dob',
		'location'
		]

class PostDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = info
		fields = [
		'id',
		'name',
		'email',
		'mobile',
		'dob',
		'location'
		]

class PostUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = info
		fields = [
		'id',
		'name',
		'email',
		'mobile',
		'dob',
		'location'
		]
