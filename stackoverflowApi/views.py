from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView )
from .models import Question
from .serializer import QuestionSerializer
from .pagination import MyPageNumberPagination
from bs4 import BeautifulSoup
import requests
from rest_framework.permissions import  IsAuthenticated



class QuestionAPI(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class    = MyPageNumberPagination

    permission_classes = [IsAuthenticated]


class QuestionCreateAPI(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
                  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)   # successfully CREATED
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # invalid data
    
    
class QuestionUpdateAPI(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    lookup_field        = 'id'                                      # set the lookup field to id


    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, id=None):
        try:                                                        # try to get the question
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)   # if not found, return 404
        
        serializer = QuestionSerializer(question)                     # serialize the question
        return Response(serializer.data)                            # return the serialized question
    
    
    def put(self, request, id=None):
        try:                                                        # try to get the question
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        serializer = QuestionSerializer(question, data=request.data)  # convert complex data by passing into serializer 
        
        if serializer.is_valid():                                   # check for validation of data
            serializer.save()
            return Response(serializer.data)                        # return updated the JSON response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # return error for invalid data


    def delete(self, request, id=None):
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)  # return 404 if not found
        
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)         # return 204 if deleted



def latest(request):
    try:
        for i in range(1,6):
            res = requests.get(f"https://stackoverflow.com/questions?tab=bounties&pagesize=50&page={i}")

            soup = BeautifulSoup(res.text, "html.parser")
            questions = soup.select(".question-summary")
            
            for que in questions:
                q = que.select_one('.question-hyperlink').getText()
                bounty = que.select_one('.bounty-indicator').getText()   
                user = que.select_one('.user-details').getText(strip=True)
                vote_count = que.select_one('.vote-count-post').getText()
                views = que.select_one('.views').attrs['title']
                tags = [i.getText() for i in (que.select('.post-tag'))]
                date = que.select_one('.relativetime').attrs['title'].split()[0]
                time_stamp = que.select_one('.relativetime').getText()
                excerpt = que.select_one('.excerpt').getText(strip=True)
                answer_status = que.select_one(".status").get_text(strip=True)
                
                question = Question()
                question.question = q
                question.bounty = bounty
                question.user = user
                question.vote_count = vote_count
                question.views = views
                question.tags = tags
                question.date = date
                question.time_stamp = time_stamp
                question.excerpt = excerpt
                question.answer_status = answer_status

                question.save()
            
                
        return HttpResponse("Latest Data Fetched from Stack Overflow")
    
    except Exception as e:
        return HttpResponse(f"Failed {e}")