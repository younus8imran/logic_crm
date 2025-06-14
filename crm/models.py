from django.db import models

# Create your models here.

class Marketing(models.Model):
    client_id = models.IntegerField(primary_key=True)
    origin = models.CharField(blank=True, null=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    address_1 = models.CharField(blank=True, null=True)
    address_2 = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    zip = models.CharField(blank=True, null=True)
    country = models.CharField(blank=True, null=True)
    campaign_code = models.CharField(blank=True, null=True)
    chain_code = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marketing'


class MailPlan(models.Model):
    date = models.DateField(blank=True, null=True)
    campaign = models.CharField(blank=True, null=True)
    chain = models.CharField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    extraction = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail_plan'


class PlanMapping(models.Model):
    code = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    sequence_no = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'plan_mapping'


class CampaignProducts(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    chain_code = models.CharField(blank=True, null=True)
    chain_name = models.CharField(blank=True, null=True)
    product_code = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    price = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaign_products'


class PaymentDetails(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    client_id = models.CharField(blank=True, null=True)
    chain_code = models.CharField(blank=True, null=True)
    campaign_code = models.CharField(blank=True, null=True)
    total_amount_entered = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True) 
    cash_amount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    check1_amount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    check1_number = models.CharField(blank=True, null=True)
    check2_amount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True) 
    check2_number = models.CharField(blank=True, null=True)
    bank = models.CharField(blank=True, null=True)
    total_cash_eur = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    total_checks_eur = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    total_card_eur = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    number_of_invoices_paid = models.IntegerField(blank=True, null=True)
    final_total_amount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    purchase_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'payment_details'


class SalesDump(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'sales_dump'

class MarketingPlan(models.Model):
    chain_name = models.CharField(max_length=50)
    marketing_code = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    sequence_no = models.IntegerField()

    class Meta:
        db_table = 'marketing_plan'
