from django.shortcuts import render, redirect
from .models import Voter, Stall
import json

def landing_page(request):
    if request.method == 'POST':
        voting_id = request.POST.get('voting_id')
        # Check if the voting ID is exactly 4 numeric digits
        if voting_id.isdigit() and len(voting_id) == 4:
            if Voter.objects.filter(voting_id=voting_id).exists():
                message = "Voting ID is already used."
            else:
                request.session['voting_id'] = voting_id  # Store voting ID in session
                return redirect('voting_page')
        else:
            message = "Invalid voting ID. Please enter 4 numeric digits."
    else:
        message = None
    return render(request, 'main/landing_page.html', {'message': message})

def voting_page(request):
    if 'voting_id' not in request.session:
        return redirect('landing_page')

    voting_id = request.session['voting_id']

    if request.method == 'POST':
        selected_stalls_str = request.POST.get('selected_stalls')
        if selected_stalls_str:  # Check if stalls are selected
            selected_stalls = json.loads(selected_stalls_str)
            selected_stalls = [int(stall) for stall in selected_stalls]
            voter = Voter.objects.create(voting_id=voting_id)  # Create voter object here
            voter.selected_stalls.add(*selected_stalls)
            for stall_num in selected_stalls:
                stall = Stall.objects.get(stall_number=stall_num)
                stall.total_votes += 1
                stall.save()
            del request.session['voting_id']  # Remove voting ID from session after processing
            return redirect('thank_you')
        else:
            del request.session['voting_id']  # Remove voting ID from session if no stalls are selected
            return redirect('voting_page')  # Redirect back to voting page

    stalls = Stall.objects.all()
    return render(request, 'main/voting_page.html', {'stalls': stalls})

def thank_you(request):
    return render(request, 'main/thank_you_page.html')
