from django.shortcuts import redirect, render
from .forms import CustomCreationForm

# Create your views here.
def signup(request):
    if request.method=='POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = CustomCreationForm()
    return render(request, 'signup.html')
