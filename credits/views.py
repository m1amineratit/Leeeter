from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import UserCredits, CreditsTransaction
from rest_framework.permissions import IsAuthenticated

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_credits(request):
    try:
        amount = float(request.data.get('amount', 0))
        if amount <= 0:
            return Response({'error' : 'Amount must be positive'}, status=400)
        
        request.user.credit.add_credits(amount)

        CreditsTransaction.objects.create(
            user=request.user,
            transaction_type='ADD',
            amount=amount,
            description='User added credits'
        )
        return Response({'message' : 'Credits added ', 'balance': request.user.credit.balance})
    
    except Exception as e:
        return Response({'error' : str(e)}, status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_balance(request):
    return Response({'balance' : request.user.credit.balance})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    transactions = CreditsTransaction.objects.filter(user=request.user).order_by('-timestamp')
    data = [{
        'type' : tx.transaction_type,
        'amount' : tx.amount,
        'description' : tx.description,
    } for tx in transactions]
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def use_credits(request):
    try:
        cost = float(request.data.get('amount', 0))
        if cost <= 0:
            return Response({'error': 'Amount must be positive'}, status=400)

        request.user.credit.deduct_credits(cost)

        CreditsTransaction.objects.create(
            user=request.user,
            transaction_type='DEDUCT',
            amount=cost,
            description='Used for feature'
        )

        return Response({
            'message': f'Deducted ${cost:.2f}',
            'remaining_balance': request.user.credit.balance
        })

    except ValueError as e:
        return Response({'error': str(e)}, status=400)
