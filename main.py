import os
from typing import List

from django.db.models.base import ModelBase

urls = '''
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]

'''


def crud_urls(model: str | ModelBase) -> str:
    str_model = str(model.__name__) if isinstance(model, ModelBase) else str(model)
    urls = f"""
    path("list/", views.{str_model.lower()}s_view, name="{str_model}s"),
    path("create/", views.{str_model.lower()}_create_view, name="create_{str_model}"),
    path("detail/<pk>/", views.{str_model.lower()}_detail_view, name="detail_{str_model}"),
    path("update/<pk>/", views.{str_model.lower()}_update_view, name="update_{str_model}"),
    path("delete/<pK>/", views.{str_model.lower()}_delete_view, name="delete_{str_model}"),
            """
    return urls


def generate_crud_urls(app_name, models):
    try:
        try:
            os.mkdir(app_name)
        except:
            pass

        with open(os.path.join(app_name, "urls.py"), "w+") as urls_file:
            print("""
from django.urls import path
from . import views


app_name = '{}'

urlpatterns = [
            """.format(app_name.lower()), file=urls_file)
            for model in models:
                str_model = str(model.__name__) if isinstance(model, ModelBase) else str(model)
                with open(os.path.join("base", "urls.py"), "rt+") as urls_base_file:
                    lines = urls_base_file.readlines()
                    for line in lines:
                        urls_file.write(line.replace("modelname", str_model.lower()))
                    urls_base_file.close()
            print("]", file=urls_file)
            urls_file.close()
    except Exception as e:
        print("*" * 10, f" {e} ", "*" * 10)
    finally:
        command = f"black {app_name}/urls.py"
        print(command)
        os.system(command)


def generate_crud_views(app_name, models):
    try:
        try:
            os.mkdir(app_name)
        except:
            pass
        with open(os.path.join(app_name, "views.py"), "w+") as file:
            print("""
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import *
from .forms import *


                """, file=file)

            for model in models:
                with open(os.path.join("base", "views.py"), "rt") as read_file:
                    str_model = str(model.__name__) if isinstance(model, ModelBase) else str(model)
                    lines = read_file.readlines()
                    print("Start procesing for {} model \n".format(str_model))
                    for line in lines:
                        print(
                            line.replace("app_name", app_name.lower()).replace("modelname", str_model.lower()).replace(
                                "ModelName", str_model).replace("\n", ""), file=file)
                    print("End procesing for {} model \n".format(
                        model.__name__ if isinstance(model, ModelBase) else model))
                read_file.close()
            file.close()
        print("Views created !")
    except:
        pass


def generate_forms(app_name: str, models: List[str | ModelBase]):

    try:
        try:
            os.mkdir(app_name)
        except:
            pass
        with open(os.path.join(app_name, "forms.py"), "w+") as forms_file:
            print("""
from django.forms import ModelForm
from . import models


                  """, file=forms_file)
            for model in models:
                str_model = str(model.__name__) if isinstance(model, ModelBase) else str(model)
                with open(os.path.join("base", "forms.py" ), "rt+") as forms_base_file:
                    lines = forms_base_file.readlines()
                    for line in lines:
                        forms_file.write(line.replace("ModelName", str_model))
                    forms_base_file.close()
            forms_file.close()
    except Exception as e:
        print(f"{e}")


generate_crud_urls(app_name="TestApp", models=["Model1", "Model2", "Model3"])
generate_crud_views(app_name="TestApp", models=["Model1", "Model2", "Model3"])
generate_forms(app_name="TestApp", models=["Model1", "Model2", "Model3"])
