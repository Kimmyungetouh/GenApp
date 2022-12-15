def modelnames_view(request: HttpRequest):
    modelnames = ModelName.objects.all()
    form = ModelNameForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _(f"{ModelName._meta.verbose_name}, created !"))
        return redirect(reverse("app_name:modelnames"))
    else:
        messages.error(
            request,
            _(f"{ModelName._meta.verbose_name}, cannot be created, an error occured !"),
        )
    context = {"modelnames": modelnames, "form": form}
    return TemplateResponse(request, "app_name/modelname/list.html", context)


def modelname_create_view(request: HttpRequest):
    form = ModelNameForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _(f"{ModelName._meta.verbose_name}, created !"))
        return redirect(reverse("app_name:modelnames"))
    else:
        messages.error(
            request,
            _(f"{ModelName._meta.verbose_name}, cannot be created, an error occured !"),
        )
    context = {"form": form}
    return TemplateResponse(request, "app_name/modelname/create.html", context)


def modelname_update_view(request: HttpRequest, pk):
    modelname = get_object_or_404(ModelName, pk=pk)
    form = ModelNameForm(request.POST or None, instance=modelname)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _(f"{ModelName._meta.verbose_name}, updated !"))
        return redirect(reverse("app_name:modelnames"))
    else:
        messages.error(
            request,
            _(f"{ModelName._meta.verbose_name}, cannot be updated, an error occured !"),
        )
    context = {"form": form, "modelname": modelname}
    return TemplateResponse(request, "app_name/modelname/update.html", context)


def modelname_delete_view(request: HttpRequest, pk):
    modelname = get_object_or_404(ModelName, pk=pk)
    try:
        modelname.delete()
        messages.success(request, _(f"{ModelName._meta.verbose_name}, deleted !"))

    except Exception as e:
        print(e)
        messages.error(
            request,
            _(f"{ModelName._meta.verbose_name}, cannot be deleted, an error occured !"),
        )
    return redirect(reverse("app_name:modelnames"))
