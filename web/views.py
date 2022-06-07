from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from web.models import *
from django.core.paginator import Paginator
from django.db.models import Q
import xlrd


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return redirect("login")


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {
        "title": "Dashboard | Education in Progress",
        "breadtitle": ""
    })


@login_required
def list(request, name):
    listmodel, title = None, ""
    if name == "schools":
        listmodel = school
        title = "Schools"
    elif name == "education-sectors":
        listmodel = educational_sector
        title = "Educational Sectors"
    elif name == "categories":
        listmodel = category
        title = "Categories"
    elif name == "coordinators":
        listmodel = coordinator
        title = "Coordinators"
    elif name == "cities":
        listmodel = city
        title = "Cities"
    elif name == "countries":
        listmodel = country
        title = "Countries"
    else:
        return render(request, "error.html", {
            "title": "Error | Education in Progress",
            "breadtitle": ""
        })
    return render(request, f"{name}.html", {
        "title": f"List {title} | Education in Progress",
        "name": title,
        "count": listmodel.objects.count(),
        "data": Paginator(listmodel.objects.all(), 10, 2).get_page(request.GET.get('page')),
        "breadtitle": "List Data"
    })


@login_required
def search(request):
    if request.method == "POST":
        filters = Q()
        if "school" in request.POST:
            if request.POST["school"] != "":
                filter = Q(id=-1)
                for item in school.objects.filter(Q(name__contains=request.POST["school"]) | Q(email__contains=request.POST["school"]) | Q(tel__contains=request.POST["school"]) | Q(address__contains=request.POST["school"]) | Q(website__contains=request.POST["school"])):
                    filter.add(Q(id=item.id), Q.OR)
                filters.add(filter, Q.AND)
        if "coordinator" in request.POST:
            if request.POST["coordinator"] != "":
                filter = Q(id=-1)
                for item in coordinator.objects.filter(Q(name__contains=request.POST["coordinator"]) | Q(email__contains=request.POST["coordinator"]) | Q(tel__contains=request.POST["coordinator"])):
                    filter.add(Q(coordinator_id=item.id), Q.OR)
                filters.add(filter, Q.AND)
        if "educational_sector" in request.POST:
            filter = Q()
            for item in request.POST.getlist("educational_sector"):
                filter.add(Q(educational_sector=item), Q.OR)
            filters.add(filter, Q.AND)
        if "category" in request.POST:
            filter = Q()
            for item in request.POST.getlist("category"):
                filter.add(Q(category=item), Q.OR)
            filters.add(filter, Q.AND)
        if "city" in request.POST:
            filter = Q()
            for item in request.POST.getlist("city"):
                filter.add(Q(city_id=item), Q.OR)
            filters.add(filter, Q.AND)
        if "country" in request.POST:
            filter = Q()
            for item in request.POST.getlist("country"):
                cities = city.objects.filter(country=item)
                for cityy in cities:
                    filter.add(Q(city_id=cityy), Q.OR)
            filters.add(filter, Q.AND)
        count = len(school.objects.filter(filters).distinct())
        data = school.objects.filter(filters).distinct()
        if count != 0:
            return render(request, "list.html", {
                "title": "Search Data | Education in Progress",
                "name": "Search",
                "count": count,
                "data": data,
                "breadtitle": "Search Data"
            })
        else:
            return render(request, "search.html", {
                "title": "Search Data | Education in Progress",
                "breadtitle": "Search Data",
                "category": category.objects.all().order_by('name'),
                "educational_sector": educational_sector.objects.all().order_by('name'),
                "city": city.objects.all().order_by('name'),
                "country": country.objects.raw("SELECT web_country.*, COUNT(web_city.id) FROM web_country INNER JOIN web_city "
                                            "ON web_country.id = web_city.country_id GROUP BY web_country.name HAVING "
                                            "COUNT(web_city.id) > 0 ORDER BY web_city.name"),
                "error": "asd",
                "schools": school.objects.all(),
                "coordinators": coordinator.objects.all()
            })
    return render(request, "search.html", {
        "title": "Search Data | Education in Progress",
        "breadtitle": "Search Data",
        "category": category.objects.all().order_by('name'),
        "educational_sector": educational_sector.objects.all().order_by('name'),
        "city": city.objects.all().order_by('name'),
        "country": country.objects.raw("SELECT web_country.*, COUNT(web_city.id) FROM web_country INNER JOIN web_city "
                                    "ON web_country.id = web_city.country_id GROUP BY web_country.name HAVING "
                                    "COUNT(web_city.id) > 0 ORDER BY web_city.name"),
        "error": "",
        "schools": school.objects.all(),
        "coordinators": coordinator.objects.all()
    })


@login_required
def file(request):
    try:
        wb = xlrd.open_workbook(request.FILES["excel"].name, file_contents=request.FILES["excel"].read())
    except:
        return render(request, "error.html", {
            "title": "Error | Education in Progress",
            "breadtitle": "",
            "error": "Sorry, an error has occured! File not suported!"
        })
    sheet = wb.sheet_by_index(0)
    if sheet.nrows > 1:
        flag = False
        for count in range(1, sheet.nrows):
            school_name = sheet.cell_value(count, 0)
            school_email = sheet.cell_value(count, 1)
            school_phone = sheet.cell_value(count, 2)
            school_address = sheet.cell_value(count, 3)
            school_website = sheet.cell_value(count, 4)
            city_name = sheet.cell_value(count, 5)
            country_name = sheet.cell_value(count, 6)
            category_name = sheet.cell_value(count, 7)
            educational_sectors = sheet.cell_value(count, 8)
            coordinator_name = sheet.cell_value(count, 9)
            coordinator_email = sheet.cell_value(count, 10)
            coordinator_phone = sheet.cell_value(count, 11)
            if country_name != "" and city_name != "" and educational_sectors != "" and school_name != "" and school_email != "" and school_phone != "" and school_website != "":
                if city.objects.filter(name=city_name).count() == 1:
                    cityy = city.objects.get(name=city_name)
                else:
                    countryy, _ = country.objects.get_or_create(name=country_name)
                    cityy, _ = city.objects.get_or_create(name=city_name, country=countryy)
                
                if category_name != "":
                    category_filter = Q()
                    for record in category_name.strip().split(";"):
                        category.objects.get_or_create(name=record)
                        category_filter.add(Q(name=record), Q.OR)
                    categoryy = category.objects.filter(category_filter)
                
                educational_sectors_filter = Q()
                for record in educational_sectors.strip().split(";"):
                    educational_sector.objects.get_or_create(name=record)
                    educational_sectors_filter.add(Q(name=record), Q.OR)
                educational_sectorss = educational_sector.objects.filter(educational_sectors_filter)
                
                if coordinator_name != "" and coordinator_email != "" and coordinator_phone != "":
                    coordinatorr, _ = coordinator.objects.get_or_create(name=coordinator_name, email=coordinator_email, tel=coordinator_phone)
                
                if school.objects.filter(name=school_name, email=school_email, tel=school_phone, website=school_website, city=cityy).count() < 1:
                    schooll = school(name=school_name, email=school_email, tel=school_phone, website=school_website, city=cityy)
                    
                    if school_address != "":
                        schooll.address=school_address

                    if coordinator_name != "" and coordinator_email != "" and coordinator_phone != "":
                        schooll.coordinator = coordinatorr
                    
                    schooll.save()
                    schooll = school.objects.get(name=school_name, email=school_email, tel=school_phone, website=school_website, city=cityy)
                    for record in educational_sectorss:
                        schooll.educational_sector.add(record)
                    if category_name != "":
                        for record in categoryy:
                            schooll.category.add(record)
                    schooll.save()
            else:
                flag = True
        if flag:
            return render(request, "error.html", {
                "title": "Error | Education in Progress",
                "breadtitle": "",
                "error": "Sorry, an error has occured! Some data is empty!"
            })
    else:
        return render(request, "error.html", {
            "title": "Error | Education in Progress",
            "breadtitle": "",
            "error": "Sorry, an error has occured! The file is empty!"
        })

    return redirect("dashboard")

def error(request):
    return render(request, "error.html", {
        "title": "Error | Education in Progress",
        "breadtitle": "",
        "error": "Sorry, an error has occured!"
    })