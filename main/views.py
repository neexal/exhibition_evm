from django.shortcuts import render, redirect
from .models import Voter, Stall
import json

def landing_page(request):
    if request.method == 'POST':
        voting_id = request.POST.get('voting_id')
        if Voter.objects.filter(voting_id=voting_id).exists():
            message = "Voting ID is already used."
        else:
            voter = Voter.objects.create(voting_id=voting_id)
            request.session['voter_id'] = voter.id
            return redirect('voting_page')
    else:
        message = None
    return render(request, 'main/landing_page.html', {'message': message})

def voting_page(request):
    if 'voter_id' not in request.session:
        return redirect('landing_page')

    voter_id = request.session['voter_id']
    voter = Voter.objects.get(pk=voter_id)

    if request.method == 'POST':
        selected_stalls_str = request.POST.get('selected_stalls')
        selected_stalls = json.loads(selected_stalls_str)
        selected_stalls = [int(stall) for stall in selected_stalls]
        voter.selected_stalls.add(*selected_stalls)
        for stall_num in selected_stalls:
            stall = Stall.objects.get(stall_number=stall_num)
            stall.total_votes += 1
            stall.save()
        return redirect('thank_you')

    # Assuming you have a list of all stalls named 'stalls'
    stalls = Stall.objects.all()
    return render(request, 'main/voting_page.html', {'stalls': stalls})

def thank_you(request):
    return render(request, 'main/thank_you_page.html')
