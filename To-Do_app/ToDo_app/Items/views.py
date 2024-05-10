from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Items, Category
from django.contrib import messages
from django.core.paginator import Paginator
import json

existingCategory = Category.objects.all()


@login_required(login_url="login")
def index(request):
    data = Items.objects.filter(owner=request.user)
    paginator = Paginator(data, 6)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    return render(
        request,
        "Items/index.html",
        {"categories": existingCategory, "values": data, "page_obj": page_obj},
    )


@login_required(login_url="login")
def addItems(request):
    viewName = "addItems"
    data = request.POST

    if request.method == "POST":
        description = data.get("description")
        category = data.get("category")
        date = data.get("date")
        owner = request.user
        newTopic = None
        newTopic = Items.objects.create(
            owner=owner,
            date=date,
            category=category,
            description=description,
        )
        newTopic.save()
        messages.success(request, "New Tasks added")
        return redirect("index")

    return render(
        request,
        "Items/addItems.html",
        {"categories": existingCategory, "values": data, "viewName": viewName},
    )


@login_required(login_url="login")
def updateItems(request):
    viewname = "updateItems"
    existingCategory = Category.objects.all()
    if request.method == "GET":
        op = request.GET
        pk = op.get("update")
        items = Items.objects.get(id=pk)
        return render(
            request,
            "Items/addItems.html",
            {"categories": existingCategory, "values": items, "viewName": viewname},
        )
    else:
        if request.method == "POST":
            data = request.POST
            pk = data.get("update")
            items = Items.objects.get(id=pk)

            description = data.get("description")
            category = data.get("category")
            date = data.get("date")
            if category:
                items.description = description
                items.category = category
                items.date = date
                messages.success(request, "Task updated")
                items.save()
                return redirect("index")
            else:
                messages.warning(request, "Category is required")
                return render(
                    request,
                    "Items/addItems.html",
                    {
                        "categories": existingCategory,
                        "values": items,
                        "viewName": viewname,
                    },
                )

        return redirect("index")


@login_required(login_url="login")
def deleteItems(request):

    print("Entered delete")
    if request.method == "POST":
        op = request.POST
        pk = op.get("delete")
        items = Items.objects.get(id=pk)
        items.delete()
        messages.info(request, "Task deleted")
        return redirect("index")


def statusItems(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pk = data.get("id")
        status = data.get("status")
        items = Items.objects.get(id=pk)
        items.status = status
        items.save()

        messages.success(request,"Status updated")
        return JsonResponse({"message": "Status updated"}, status=200)
