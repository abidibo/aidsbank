# coding=utf-8
from django.db import models
from django.db.models import permalink
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

"""
Centre model
"""
class Centre(models.Model):
    name = models.CharField('nome', max_length=255)
    address = models.CharField('indirizzo', max_length=255)
    city = models.CharField('città', max_length=255)
    cap = models.CharField('cap', max_length=5)
    phone = models.CharField('telefono', max_length=32)
    fax = models.CharField('fax', max_length=32, blank=True, null=True)
    email = models.EmailField('email')
    description = RichTextField(verbose_name = 'descrizione', blank=True, null=True)
    timetable = RichTextField(verbose_name = 'orari')
    notes = models.TextField('note', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'centro'
        verbose_name_plural = 'centri'
        ordering = ('name',)

"""
Manager
"""
class Manager(models.Model):
    user = models.ForeignKey(User, verbose_name='utente')
    centres = models.ManyToManyField(Centre, verbose_name='centri')

    def get_centres_display(self):
        return ', '.join([c.name for c in self.centres.all()])
    get_centres_display.short_description = 'centri'

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = 'referente'
        verbose_name_plural = 'referenti'

"""
Applicant
"""
class Applicant(models.Model):
    user = models.ForeignKey(User, verbose_name='utente')
    address = models.CharField('indirizzo', max_length=128)
    city = models.CharField('città', max_length=128)
    cap = models.IntegerField('cap', max_length=5)
    province = models.CharField('provincia', max_length=128)
    phone = models.CharField('telefono', max_length=32, blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    @permalink
    def get_absolute_url(self):
        return ('applicant_profile', None, {})

    def get_loans(self):
        return Loan.objects.filter(applicant=self).order_by('-reservation_date')

    class Meta:
        verbose_name = 'richiedente'
        verbose_name_plural = 'richiedenti'

"""
Aid type
"""
class AidType(models.Model):
    name = models.CharField('nome', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'tipologia ausilio'
        verbose_name_plural = 'tipologie ausilio'

"""
Aid
"""

""" Path to the upload folder for aids """
def set_aid_folder(instance, filename):
    return '/'.join([settings.MEDIA_AID_REL, filename])

class Aid(models.Model):
    type = models.ForeignKey(AidType, verbose_name = 'tipologia')
    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug per url', max_length=255)
    code = models.CharField('codice', max_length=255)
    description = RichTextField(verbose_name = 'descrizione')
    card = models.FileField(verbose_name='scheda pdf', upload_to=set_aid_folder, blank=True, null=True)
    deposit = models.DecimalField('cauzione', max_digits=8, decimal_places=2)
    max_loan_duration = models.IntegerField('durata massima prestito', help_text='mesi', max_length=4)
    notes = models.TextField('note', blank=True, null=True)

    def __unicode__(self):
        return self.code

    @permalink
    def get_absolute_url(self):
        return ('aid_detail', None, {
          'slug': self.slug,
        })

    class Meta:
        verbose_name = 'ausilio'
        verbose_name_plural = 'ausili'

"""
Asset
"""
class Asset(models.Model):
    aid = models.ForeignKey(Aid, verbose_name = 'ausilio')
    centre = models.ForeignKey(Centre, verbose_name = 'centro')
    code = models.CharField('codice', max_length=255)
    vendor = models.CharField('fornitore', max_length=255)
    invoice_number = models.CharField('numero fattura', max_length=255, blank=True, null=True)
    invoice_date = models.DateField('data fattura', blank=True, null=True)
    price = models.DecimalField('prezzo', max_digits=8, decimal_places=2, blank=True, null=True)
    color = models.CharField('colore', max_length=64, blank=True, null=True)
    condition = models.IntegerField('condizioni', choices=settings.AIDSBANK_ASSET_CONDITION_CHOICES, blank=True, null=True)
    loan_available = models.BooleanField('prestito', help_text='spuntare se disponibile per il prestito')
    notes = models.TextField('note', blank=True, null=True)

    def __unicode__(self):
        return self.code

    def get_status(self):
        return 'lala';

    def availability_info(self):
        if not self.loan_available:
            return 'no'
        else:
            return 'si'

    def get_status(self):
        movements = Movement.objects.filter(asset=self).order_by('-id')
        if(movements):
            return movements[0].get_status_display()
        else:
            return None

    class Meta:
        verbose_name = 'cespite'
        verbose_name_plural = 'cespiti'
        permissions = (
            ('view_asset_loan_unavailable', 'visualizza cespiti non disponibili per il prestito'),
            ('view_asset_availability', 'visualizza disponibilità'),
            ('publish_asset_comments', 'pubblicazione commenti'),
            ('moderate_asset_comments', 'moderazione commenti'),
            ('send_asset_request', 'invio richiesta cespite'),
        )

"""
Loan
"""
class Loan(models.Model):
    asset = models.ForeignKey(Asset, verbose_name = 'cespite')
    applicant = models.ForeignKey(Applicant, verbose_name='richiedente')
    addressee = models.CharField('destinatario', max_length=128, blank=True, null=True)
    place = models.CharField('luogo destinazione', max_length=128, blank=True, null=True)
    deposit = models.DecimalField('cauzione', max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.IntegerField('stato', choices=settings.AIDSBANK_LOAN_STATUS_CHOICES, max_length=1)
    reservation_date = models.DateField('data di prenotazione')
    loan_date = models.DateField('data prestito', blank=True, null=True)
    loan_duration = models.IntegerField('durata prestito', help_text='mesi', max_length=8, blank=True, null=True)
    renewal_date = models.DateField('data rinnovo', blank=True, null=True)
    return_date = models.DateField('data restituzione', blank=True, null=True)
    solicit_date = models.DateField('data sollecito', blank=True, null=True)
    follow_up = models.CharField('follow up', max_length=128, blank=True, null=True)
    notes = models.TextField('note', blank=True, null=True)
    renewal_available = models.BooleanField('rinnovo disponibile', blank=True, default=True)

    def __unicode__(self):
        return '%s - %s' % (self.id, self.asset.code)

    class Meta:
        verbose_name = 'prestito'
        verbose_name_plural = 'prestiti'

"""
Movement
"""
class Movement(models.Model):
    asset = models.ForeignKey(Asset, verbose_name = 'cespite')
    manager = models.ForeignKey(Manager, verbose_name='referente')
    date = models.DateField('data')
    type = models.IntegerField(verbose_name='tipo movimento', choices=settings.AIDSBANK_MOVEMENT_TYPE_CHOICES, null=True, blank=True)
    loan = models.ForeignKey(Loan, verbose_name='prestito', blank=True, null=True)
    status = models.IntegerField(verbose_name='stato', choices=settings.AIDSBANK_MOVEMENT_LAST_STATUS_CHOICES, null=True, blank=True)
    notes = models.TextField('note', blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.date, self.asset.code)

    class Meta:
        verbose_name = 'movimento'
        verbose_name_plural = 'movimenti'

"""
Asset comment
"""
class AssetComment(models.Model):
    asset = models.ForeignKey(Asset, verbose_name = 'cespite')
    applicant = models.ForeignKey(Applicant, verbose_name='richiedente')
    date = models.DateTimeField('data')
    text = models.TextField('testo');
    published = models.BooleanField('pubblicato');

    def __unicode__(self):
        return 'commento cespite %s, utente %s %s' % (self.asset.code, self.applicant.first_name, self.applicant.last_name)

    class Meta:
        verbose_name = 'commento'
        verbose_name_plural = 'commenti'

