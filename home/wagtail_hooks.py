from django.utils.safestring import mark_safe
from wagtail import hooks


@hooks.register("insert_global_admin_js")
def get_global_admin_js():
    return mark_safe(
    """
    <script>
        window.addEventListener('DOMContentLoaded', function () {
            document.addEventListener('wagtail:images-upload', function(event) {
                const now  = new Date();
                date_string = [
                    now.getDate(), ".",
                    now.getMonth(), ".",
                    now.getFullYear(), " ",
                    now.getHours(), ":",
                    now.getMinutes()
                ].join('');

                event.detail.data.title = date_string;
            });
        });
    </script>
    """
    )