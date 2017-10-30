from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class EmailTemplate(EmailMultiAlternatives):

    def __init__(self, tpl_message, context, tpl_alternative=None, **kwargs):
        super(EmailTemplate, self).__init__(**kwargs)
        self.message_from_template(tpl_message, context)
        if tpl_alternative:
            self.attach_alternative_from_template(tpl_alternative, context)

    def message_from_template(self, template, context):
        self.body = render_to_string(template, context)

    def attach_alternative_from_template(self, template, context):
        content = render_to_string(template, context)
        self.attach_alternative(content, 'text/html')
