import argparse, os

import django

from gen_utils import generate_crud_urls, generate_crud_views, generate_forms, get_apps

# from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

parser = argparse.ArgumentParser()

# parser.add_argument("--app_name", help="Enter your app_name")
parser.add_argument(
    "--app_dir", help="The name of the directory where your apps are located to"
)
parser.add_argument(
    "--app_clone_dir", help="The name of the directory where you want to clone apps"
)
parser.add_argument(
    "--gen_template_dir", help="The name of the directory where you want to clone apps"
)

args = parser.parse_args()
# app_name, app_dir = args.app_name, args.app_dir
app_dir, app_clone_dir, gen_template_dir = (
    args.app_dir,
    args.app_clone_dir or "app_clones",
    args.gen_template_dir or "base",
)


try:
    os.mkdir(app_dir)
    os.rmdir(app_dir)
except FileExistsError:
    pass

try:

    os.mkdir(os.path.join(app_dir, app_clone_dir))
except FileExistsError as e:
    print(f"{app_clone_dir} exists !")

for app_to_process in get_apps(app_dir):
    print("Generating crud for {} ...".format(app_to_process))
    os.chdir(os.path.join(app_dir, app_clone_dir))
    generate_crud_urls(
        app_name=app_to_process, gen_template_dir=f"../{gen_template_dir}"
    )
    generate_crud_views(
        app_name=app_to_process, gen_template_dir=f"../{gen_template_dir}"
    )
    generate_forms(app_name=app_to_process, gen_template_dir=f"../{gen_template_dir}")
    os.chdir("../..")
