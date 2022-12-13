import argparse, os
from gen_utils import generate_crud_urls, generate_crud_views, generate_forms

parser = argparse.ArgumentParser()

# parser.add_argument("--app_name", help="Enter your app_name")
parser.add_argument("--app_dir", help="The name of the directory where your apps are located to")
# parser.add_argument("--app_clone", help="The name of the directory where you want to clone apps")

args = parser.parse_args()
# app_name, app_dir = args.app_name, args.app_dir
app_name, app_dir = args.app_name, args.app_dir


try:
    os.mkdir(os.path.join(app_dir, "apps_clones"))
except FileExistsError as e:
    print("")

generate_crud_urls(app_name=app_name, app_dir=app_dir)
generate_crud_views(app_name=app_name, app_dir=app_dir)
generate_forms(app_name=app_name, app_dir=app_dir)
