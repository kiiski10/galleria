# 2fa fix

`wagtail-2fa` does not work with Wagtail versions 6 and above.
There is [issue #228](https://github.com/labd/wagtail-2fa/issues/228) with working suggestion how to fix this in the template `site-packages/wagtail_2fa/templates/wagtail_2fa/otp_form.html`. Until the fix is merged the template must be patched manually after installing the `wagtail-2fa` python package.