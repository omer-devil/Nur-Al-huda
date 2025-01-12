# =========================================================================== #
# Author: Omer Kemal                                                          #
# Social Media:                                                               #
#   - Facebook: https://web.facebook.com/omer.kemal.7                         #
#   - GitHub: https://github.com/omer-devil                                   #
# =========================================================================== #

from flask import Blueprint, url_for, render_template

from database.manage_db import var

public = Blueprint(
    'public', __name__,
    static_folder=var.STATIC_FOLDE, static_url_path=var.STATIC_FOLDE_PATH, template_folder=var.TEMPLATE_FOLDER
)


@public.route('/')
def index():
    return render_template('index.html')

@public.route("/about")
def about():
    pass
