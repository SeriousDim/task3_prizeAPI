from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Promo, Participant, Prize, Result
from random import shuffle


@api_view(['GET', 'POST'])
def promo(request):
    if request.method == 'GET':
        promos = Promo.objects.all()
        answer = []
        for p in promos:
            answer.append({"id": p.id,
                           "name": p.name,
                           "description": p.description})
        return Response(data=answer, status=200)
    if request.method == 'POST':
        data = request.data
        if 'name' not in data:
            return Response(data="Нет обязательного параметра name", status=400)
        desc = ""
        if 'description' in data:
            desc = data['description']
        promo = Promo(name=data['name'], description=desc)
        promo.save()
        return Response(data=promo.id, status=201)


@api_view(['GET'])
def specific_promo(request, id):
    promo = Promo.objects.get(id=id)
    if promo is None:
        return Response("Нет такой промоакции", status=404)
    answer = {}
    answer['id'] = promo.id
    answer['name']  = promo.name
    answer['description'] = promo.description
    answer['prizes'] = []
    answer['participants'] = []
    prizes = promo.prizes
    parts = promo.participants
    for p in prizes:
        answer['prizes'].append({"id": p.id,
                                 "description": p.description})
    for p in parts:
        answer['participants'].append({"id": p.id,
                                       "name": p.name})
    return Response(data=answer, status=200)


@api_view(['PUT'])
def edit_promo(request, id):
    promo = Promo.objects.get(id=id)
    if promo is None:
        return Response("Нет такой промоакции", status=404)
    data = request.data
    if 'name' in data:
        promo.name = data['name']
    if 'description' in data:
        promo.description = data['description']
    promo.save("Успешно", status=200)


@api_view(['DELETE'])
def delete_promo(request, id):
    promo = Promo.objects.get(id=id)
    if promo is None:
        return Response("Нет такой промоакции", status=404)
    promo.delete()
    promo.save("Успешно", status=200)


@api_view(['POST'])
def add_part(request, id):
    promo = Promo.objects.get(id=id)
    if promo is None:
        return Response("Нет такой промоакции", status=404)
    if 'name' not in request.data:
        return Response("Вы не указали имя", status=404)
    participant = Participant(name = request.data['name'])
    participant.save()
    promo.participants.add(participant)
    promo.save()
    return Response(data=participant.id, status=200)


@api_view(['DELETE'])
def delete_part(request, promo_id, part_id):
    promo = Promo.objects.get(id=promo_id)
    if promo is None:
        return Response("Нет такой промоакции", status=404)
    participant = Participant.objects.get(id = part_id)
    if participant is None:
        return Response("Нет такой участника", status=404)
    promo.participants.remove(participant)
    participant.save()
    promo.save()
    return Response(data="Успешно", status=200)


@api_view(['POST'])
def prize(request, id):
    promo = Promo.objects.get(id=id)
    if promo is None:
        return Response("Нет такой промоакции", status=404)
    if 'description' not in request.data:
        return Response("Вы не указали описание", status=404)
    prize = Prize(description=request.data['description'])
    prize.save()
    promo.prizes.add(prize)
    promo.save()
    return Response(data=prize.id, status=200)


@api_view(['DELETE'])
def delete_prize(request, promo_id, prize_id):
    promo = Promo.objects.get(id=promo_id)
    if promo is None:
        return Response("Нет такой промоакции", status=404)
    prize = Prize.objects.get(id=prize_id)
    if prize is None:
        return Response("Нет такого приза", status=404)
    promo.prizes.remove(prize)
    promo.save()
    prize.save()
    return Response(data="Успешно", status=200)


@api_view(['POST'])
def start(id):
    promo = Promo.objects.get(id=id)
    if promo is None:
        return Response("Нет такой промоакции", status=404)
    parts = promo.participants
    prizes = promo.prizes
    if len(parts) == 0 or len(prizes == 0) or \
        len(parts) != len(prizes):
        return Response(data="Проведение розыгрыша пока невозможно", status=409)
    pta = []
    pza = []
    for i in parts:
        pta.append({"id": i.id,
                "name": i.name})
    for j in prizes:
        pza.append({"id": j.id,
               "description": j.description})

    result = []
    shuffle(pta)
    for idx in range(len(pta)):
        result.append({
            "winner": {"id": pta[idx].id, "name": pta[idx].name},
            "prize": {"id": pza[idx].id, "description": pza[idx].description}
        })
    return Response(data=result, status=200)

