from django.shortcuts import render

from myWeb.models import About, Education, Work, Project, Contact, SystemInfo, Testimonials


def portfolio_view(request):
    about = About.objects.first()
    education = Education.objects.all()
    work = Work.objects.all()
    project = Project.objects.all()
    contact = Contact.objects.first()
    system_info = SystemInfo.objects.first()
    testimonials = Testimonials.objects.all()

    context = {
        'about': about,
        'education': education,
        'work': work,
        'project': project,
        'contact': contact,
        'system_info': system_info,
        'testimonials': testimonials
    }


    return render(request, 'portfolio.html', context)
