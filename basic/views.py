from django.shortcuts import render
from django.http import Http404
from .models import Computed, PrimeCheck
from django.utils import timezone
from django.http import HttpResponse


# Create your views here.

# Computation function
# Computes the square of the given value.
# If the square of value has been computed before, it retrieves
# it from the database. Otherwise it computes the square and 
# stores it into the database.
# URL pattern: path('compute/<str:value>', views.compute, name='compute')
def compute(request, value):
    try:
        input = int(value)
        precomputed = Computed.objects.filter(input=input)
        if precomputed.count() == 0:  # square has not been computed
            # Compute the square
            answer = input * input
            time_computed = timezone.now()
            # Create a Computed object and store it
            computed = Computed(
                input=input, 
                output=answer,
                time_computed=time_computed
            )
            computed.save() # Saves the object into the database
        else: 
            # Retrieve the precomputed value
            computed = precomputed.first()
        
        # Return the result page
        return render (
            request,
            "basic/compute.html", # Template html file; contains placeholders for output
            {
                'input': input,
                'output': computed.output,
                'time_computed': computed.time_computed.strftime("%m-%d-%Y %H:%M:%S UTC")
            }
        )
    except:
        raise Http404(f"Invalid input: {value}")

def is_prime_number(n):
    if n < 2:
        return False, None
    if n == 2:
        return True, None
    if n % 2 == 0:
        return False, 2
    
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False, i
        i += 2
    return True, None

def is_prime(request, number):
    try:
        input_number = int(number)
        precomputed = PrimeCheck.objects.filter(input=input_number)
        
        if precomputed.count() == 0:
            result, divisor = is_prime_number(input_number)
            prime_check = PrimeCheck(
                input=input_number,
                is_prime=result,
                divisor=divisor
            )
            prime_check.save()
        else:
            prime_check = precomputed.first()
        
        return render(
            request,
            "basic/isprime.html",
            {
                'input': input_number,
                'is_prime': prime_check.is_prime,
                'divisor': prime_check.divisor
            }
        )
    except:
        raise Http404(f"Invalid input: {number}")