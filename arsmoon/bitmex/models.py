from django.db import models
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    name = models.CharField(_('Account name'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    api_key = models.CharField(_('API KEY'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    api_secret = models.CharField(_('API SECRET'), max_length=255, help_text=_('Maximum length is 255 symbols'))

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Account')

    def __str__(self):
        return self.name


class ClientAccountCounter(models.Model):
    count = models.IntegerField(_('Number of connections'), default=0)
    account = models.ForeignKey(Account, verbose_name=_('ClientAccountCounter'), on_delete=models.CASCADE)
    task_id = models.CharField(_('Task_id'), max_length=255, help_text=_('Maximum length is 255 symbols'))

    def __str__(self):
        return self.account.name
