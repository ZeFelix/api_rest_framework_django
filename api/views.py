from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .serializer import VagaSerializer
from .models import *
from django.core.exceptions import ObjectDoesNotExist

from api.pagination import PaginacaoVagas

# Create your views here.

class VagaList(APIView):
    def get(self,request):
        try:
            lista_vagas = Vaga.objects.all()
            paginator = PaginacaoVagas()
            result_page = paginator.paginate_queryset(lista_vagas,request)
            serializer = VagaSerializer(result_page,many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            return JsonResponse({"mensagem":"Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def post(self,request):
        try:
            serializer = VagaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"mensagem":"Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class VagaDetalhes(APIView):
    def delete(self,request,pk):
        try:
            if pk == "0":
                return JsonResponse({"mensagem":"O ID deve ser maior que zero."},
                                    status=status.HTTP_400_BAD_REQUEST)
            vaga = Vaga.objects.get(pk=pk)
            vaga.delete()
            return Response({"mensagem":"Vaga removida!"},status=status.HTTP_204_NO_CONTENT)            
        except ObjectDoesNotExist:
            return JsonResponse({"mensagem":"A vaga não existe"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({"mensagem":"Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request,pk):
        try:
            if pk == "0":
                return JsonResponse({"mensagem":"O ID deve ser maior que zero."},
                                    status=status.HTTP_400_BAD_REQUEST)
            vaga = Vaga.objects.get(pk=pk)
            serializer = VagaSerializer(vaga)
            return Response(serializer.data)            
        except ObjectDoesNotExist:
            return JsonResponse({"mensagem":"A vaga não existe"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({"mensagem":"Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            if pk == "0":
                return JsonResponse({"mensagem":"O ID deve ser maior que zero."},
                                    status=status.HTTP_400_BAD_REQUEST)
            vaga = Vaga.objects.get(pk=pk)
            serializer = VagaSerializer(vaga,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)                                
        except ObjectDoesNotExist:
            return JsonResponse({"mensagem":"A vaga não existe"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({"mensagem":"Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)