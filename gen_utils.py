import os
from django.conf import settings
from django.db.models.base import ModelBase
from django.apps import apps

excluded = []


def get_apps(app_dir: str):
    app_list = []
    os.chdir(app_dir)
    for potential_app in os.listdir():
        try:
            os.chdir(potential_app)
            for fs_object in os.listdir():
                if fs_object == "apps.py":
                    app_list.append(potential_app)
            os.chdir("..")
        except NotADirectoryError as e:
            print(f"{e}")
    os.chdir("..")
    installed_app_list = [app.split(".")[-1] for app in settings.INSTALLED_APPS]
    app_list = [app for app in app_list if app in installed_app_list]
    print(app_list)
    return app_list


def get_models_name(app_name):
    app_config = apps.get_app_config(app_name)
    models = app_config.models.values()
    models_names = [model.__name__ for model in models]
    try:
        models_names = [model for model in models_names if not model in excluded]
    except NameError as e:
        print(f"{e}")
    return models_names


def generate_crud_urls(app_name, gen_template_dir):
    models = get_models_name(app_name)
    try:
        try:
            os.mkdir(app_name.lower())
        except:
            pass

        with open(os.path.join(app_name, "urls.py"), "w+") as urls_file:
            print(
                """
from django.urls import path
from . import views


app_name = '{}'

urlpatterns = [
            """.format(
                    app_name.lower()
                ),
                file=urls_file,
            )
            for model in models:
                with open(
                    os.path.join(gen_template_dir, "urls.py"), "rt+"
                ) as urls_base_file:
                    lines = urls_base_file.readlines()
                    for line in lines:
                        urls_file.write(line.replace("modelname", model.lower()))
                    urls_base_file.close()
            print("]", file=urls_file)
            urls_file.close()
    except Exception as e:
        print("*" * 10, f" {e} ", "*" * 10)
    finally:
        command = f"black {app_name}/urls.py"
        print(command)
        os.system(command)


def generate_crud_views(app_name, gen_template_dir):
    models = get_models_name(app_name)
    try:
        try:
            os.mkdir(app_name.lower())
        except:
            pass
        with open(os.path.join(app_name, "views.py"), "w+") as file:
            print(
                """
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import *
from .forms import *


                """,
                file=file,
            )

            for model in models:
                with open(
                    os.path.join(gen_template_dir, "views.py"), "rt"
                ) as read_file:
                    lines = read_file.readlines()
                    print("Start procesing for {} model \n".format(model))
                    for line in lines:
                        print(
                            line.replace("app_name", app_name.lower())
                            .replace("modelname", model.lower())
                            .replace("ModelName", model)
                            .replace("\n", ""),
                            file=file,
                        )
                    print(
                        "End procesing for {} model \n".format(
                            model.__name__ if isinstance(model, ModelBase) else model
                        )
                    )
                read_file.close()
            file.close()
        print("Views created !")
    except:
        pass
    finally:
        command = f"black {app_name}/views.py"
        print(command)
        os.system(command)


def generate_forms(app_name: str, gen_template_dir: str):
    models = get_models_name(app_name)
    try:
        try:
            os.mkdir(app_name.lower())
        except:
            pass
        with open(os.path.join(app_name, "forms.py"), "w+") as forms_file:
            print(
                """
from django.forms import ModelForm
from models import *


                  """,
                file=forms_file,
            )
            for model in models:
                with open(
                    os.path.join(gen_template_dir, "forms.py"), "rt+"
                ) as forms_base_file:
                    lines = forms_base_file.readlines()
                    for line in lines:
                        forms_file.write(line.replace("ModelName", model))
                    forms_base_file.close()
            forms_file.close()
    except Exception as e:
        print(f"{e}")
    finally:
        command = f"black {app_name}/forms.py"
        print(command)
        os.system(command)
