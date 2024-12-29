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
                const month = String(now.getMonth() + 1).padStart(2, '0');
                const day = String(now.getDate()).padStart(2, '0');
                const minutes = String(now.getMinutes()).padStart(2, "0");
                date_string = [
                    day, ".",
                    month, ".",
                    now.getFullYear(), " ",
                    now.getHours(), ":",
                    minutes
                ].join('');

                event.detail.data.title = date_string;
            });
        });
    </script>
    """
    )