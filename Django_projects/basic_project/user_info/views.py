from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import info

from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	UpdateAPIView,
	RetrieveAPIView
	)

from .serializers import (
	PostCreateSerializer,
	PostDetailsSerializer,
	PostListSerializer,
	PostUpdateSerializer
	)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def index(request):
	
	info_list = info.objects.all()
	context = {'info_list' : info_list}
	return render(request, 'user_list/index.html', context)	

def details(request):
	return render(request, 'user_list/details.html')

def edit(request):
	return render(request, 'user_list/add_edit.html')

class PostCreateAPIView(CreateAPIView):
	queryset = info.objects.all()
	serializer_class = PostCreateSerializer


class PostDetailsAPIView(RetrieveAPIView):
	queryset = info.objects.all()
	serializer_class = PostDetailsSerializer
	#lookup_field = 'id'

class PostUpdateAPIView(UpdateAPIView):
	queryset = info.objects.all()
	serializer_class = PostUpdateSerializer
	#lookup_field = 'id'

class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer

	def get_queryset(self, *args, **kwargs):
		try:
			query = self.request.GET.get("page")
			query = (int(query)-1)*5
			queryset = info.objects.raw("select * from user_info_info limit 5 offset "+str(query))
			return queryset
		except info.DoesNotExist:
			return "error"
