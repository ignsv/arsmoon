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

    def __str__(self):
        return self.account.name


class Order(models.Model):
    orderID = models.CharField(_('BitMex order id'), max_length=255, help_text=_('Maximum length is 255 symbols'),
                               unique=True)
    symbol = models.CharField(_('BitMex Symbol'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    volume = models.FloatField('Bitmex volume')
    timestamp = models.DateTimeField('BitMex timestamp')
    side = models.CharField(_('BitMex side'), max_length=255, help_text=_('Maximum length is 255 symbols'))
    price = models.FloatField('Bitmex price')
    account = models.ForeignKey(Account, verbose_name=_('ClientAccountCounter'), on_delete=models.CASCADE,
                                related_name='orders')
