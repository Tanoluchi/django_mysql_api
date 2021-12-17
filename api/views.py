from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import json

from .models import Company

# Create your views here.
class CompanyView(View):
    # Agregamos un decorador para saltarnos el csrf
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Listar las compañias
    def get(self, request, id=0):
        if (id > 0):
            companies = list(Company.objects.filter(id=id).values())
            if len(companies) > 0:
                company = companies[0]
                data = {'message': "Success", 'company': company}
            else:
                data = {'message': "Companies not found..."}

            return JsonResponse(data)
        else:
            # Lo convertimos a una lista para serializarlo a un JSON
            companies = list(Company.objects.values())
            if len(companies) > 0:
                data = {'message': "Success", 'companies': companies}
            else:
                data = {'message': "Companies not found..."}

            return JsonResponse(data)

    # Creacion de registro y envio de datos
    def post(self, request):
        # Transformamos en un diccionario de Python los datos enviados en el metodo POST
        jd = json.loads(request.body)
        # Creamos un nuevo elemento y insertamos los datos enviados por el metodo POST
        Company.objects.create(name=jd['name'], website=jd['website'], foundation=jd['foundation'])
        data = {'message': "Success"}

        return JsonResponse(data)

    # Actualizacion de los datos
    def put(self, request, id):
        jd = json.loads(request.body)
        companies = list(Company.objects.filter(id=id).values())

        # Verificamos si existe al menos un dato en nuestra variable
        if len(companies) > 0:
            # Traemos el objeto que sea igual al id proporcionado por el usuario
            company = Company.objects.get(id=id)
            # Actualizamos sus campos
            company.name=jd['name']
            company.website=jd['website']
            company.foundation=jd['foundation']
            # Guardamos los cambios
            company.save()
            data = {'message': "Success"}

        else:
            data = {'message': "Companies not found..."}

        return JsonResponse(data)
    def delete(self, request, id):
        # Buscamos el dato que coincida con el id proporcionado
        companies = list(Company.objects.filter(id=id).values())
        # Verificamos de que exista, si existe borramos.
        if len(companies) > 0:
            # Traemos el elemento que coincida con el id proporcionado y lo borramos.
            Company.objects.filter(id=id).delete()
            data = {'message': "Success"}
        else:
            data = {'message': "Companies not found..."}

        return JsonResponse(data)
