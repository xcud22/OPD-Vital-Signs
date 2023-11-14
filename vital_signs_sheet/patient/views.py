from django.shortcuts import render
from.forms import PersonForm
from.models import Person

def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            form = PersonForm()  # Create a new form instance
    else:
        form = PersonForm()

    persons = Person.objects.all()
    
    #return render(request, 'create_person.html', {'form': form})
    return render(request, 'create_person.html', {'form': form, 'persons': persons})
