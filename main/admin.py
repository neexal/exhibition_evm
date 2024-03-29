from django.contrib import admin
from .models import Stall, Voter

class StallAdmin(admin.ModelAdmin):
    list_display = ('stall_number', 'total_votes')  # Displaying stall_number and total_votes in the admin panel
    ordering = ('total_votes',)  # Default sorting by total_votes
    list_filter = ('total_votes',)  # Adding filter by total_votes

admin.site.register(Stall, StallAdmin)


# class VoterAdmin(admin.ModelAdmin):
#     list_display = ('voting_id', ) 
#     list_filter = ('voting_id',)  

# admin.site.register(Voter, VoterAdmin)

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'display_selected_stalls')  # Define the fields to display in the list view

    def display_selected_stalls(self, obj):
        return ", ".join([str(stall.stall_number) for stall in obj.selected_stalls.all()])  # Display selected stalls as a comma-separated list

    display_selected_stalls.short_description = 'Selected Stalls'  # Set a custom column header for the selected stalls
