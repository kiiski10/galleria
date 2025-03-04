# 2fa fix

`wagtail-2fa` does not work with Wagtail versions 6 and above.
There is [issue #228](https://github.com/labd/wagtail-2fa/issues/228) with working suggestion how to fix this in the template `site-packages/wagtail_2fa/templates/wagtail_2fa/otp_form.html`. Until the fix is merged the template must be patched manually after installing the `wagtail-2fa` python package.

# First run

## To start up the gallery app

- Activate the virtual environment `source venv/bin/activate`
- Run migrations `python manage.py migrate`
- Replace wagtail initial data with gallery data `python manage.py initial-data`
- Create superuser to the login to site with `python manage.py createsuperuser`
- Set up the 2fa authentication by logging in the sites `/admin/` and following the instructions
- In the admin view use left menu panel to navigate to `Pages` -> `Juuri`
- Click + -button to create a `Child page`. Select `Image page` as the type
- Give the page a title and a body that you want to show in the page
- Click `Choose an image` and upload or use already uploaded image for the page