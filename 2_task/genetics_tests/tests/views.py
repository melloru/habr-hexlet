from django.shortcuts import render, redirect, get_object_or_404
from .models import GeneticTest
from .forms import GeneticTestForm
from django.db.models import Count, Avg, Max, Q


def genetic_test_list(request):
    selected_species = request.GET.get('species', '')
    tests = GeneticTest.objects.all()

    if selected_species:
        tests = tests.filter(species=selected_species)

    species_list = GeneticTest.objects.values_list('species', flat=True).distinct()

    return render(request, 'tests/genetic_test_list.html', {
        'tests': tests,
        'species_list': species_list,
        'selected_species': selected_species,
    })


def genetic_test_create(request):
   if request.method == 'POST':
       form = GeneticTestForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('genetic_test_list')
   else:
       form = GeneticTestForm()
   return render(request, 'tests/genetic_test_form.html', {'form': form})


def genetic_test_edit(request, pk):
    test = get_object_or_404(GeneticTest, pk=pk)
    if request.method == 'POST':
       form = GeneticTestForm(request.POST, instance=test)
       if form.is_valid():
           form.save()
           return redirect('genetic_test_list')
    else:
       form = GeneticTestForm(instance=test)
    return render(request, 'tests/genetic_test_form.html', {'form': form})


def genetic_test_delete(request, pk):
    test = get_object_or_404(GeneticTest, pk=pk)
    if request.method == 'POST':
        test.delete()
        return redirect('genetic_test_list')
    return render(request, 'tests/genetic_test_confirm_delete.html', {'test': test})


def statistics(request):
    # Получаем статистику по видам животных
    statistics_data = (
        GeneticTest.objects
        .values('species')
        .annotate(
            total_tests=Count('id'),
            avg_milk_yield=Avg('milk_yield'),
            max_milk_yield=Max('milk_yield'),
            good_health_count=Count(Q(health_status='good'))
        )
    )

    statistics_list = []
    for data in statistics_data:
        total_tests = data['total_tests']
        good_health_count = data['good_health_count']

        good_health_percentage = (good_health_count / total_tests * 100) if total_tests > 0 else 0

        statistics_list.append({
            'species': data['species'],
            'total_tests': total_tests,
            'avg_milk_yield': data['avg_milk_yield'] if data['avg_milk_yield'] is not None else 0,
            'max_milk_yield': data['max_milk_yield'] if data['max_milk_yield'] is not None else 0,
            'good_health_percentage': good_health_percentage,
        })

    return render(request, 'tests/statistics.html', {'statistics': statistics_list})
