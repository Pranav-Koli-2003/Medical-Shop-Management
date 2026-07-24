from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
#userData 
class User(models.Model):
    usertokenId = models.IntegerField()
    userID = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=50)
    shopName = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.username


#purchase Medicine

class Purchase_Company(models.Model):
    purchase_user_company_token = models.IntegerField()
    purchase_compnay_token = models.IntegerField()
    purchase_compnay_name = models.CharField(max_length=50)
    purchase_compnay_address = models.CharField(max_length=250)
    purchase_compnay_phone = models.CharField(max_length=50)
    purchase_compnay_state_code = models.CharField(max_length=50)
    purchase_compnay_gstin = models.CharField(max_length=50)
    purchase_compnay_pan = models.CharField(max_length=50)
    purchase_compnay_DL_no = models.CharField(max_length=50)
    purchase_invoice_no = models.CharField(max_length=50)
    purchase_date = models.DateField()
    purchase_Dul_bal = models.CharField(max_length=50)
    purchase_POno = models.CharField(max_length=50)
    purchase_salesman = models.CharField(max_length=50)
    purchase_Gross = models.CharField(max_length=50)
    purchase_CGST = models.CharField(max_length=50)
    purchase_CGST_Taxable = models.CharField(max_length=50)
    purchase_CGST_TaxAmt = models.CharField(max_length=50)
    purchase_SGST = models.CharField(max_length=50)
    purchase_SGST_Taxable = models.CharField(max_length=50)
    purchase_SGST_TaxAmt = models.CharField(max_length=50)
    purchase_Total_GST = models.CharField(max_length=50)
    purchase_Total_Disc = models.CharField(max_length=50)
    purchase_Less = models.CharField(max_length=50)
    purchase_Add = models.CharField(max_length=50)
    purchase_NET = models.CharField(max_length=50)

    def __str__(self):
        return self.purchase_compnay_name


class Purchase_Medicine_data(models.Model):
    purchase_user_medicine_token = models.IntegerField()
    purchase_medicine_token = models.IntegerField()
    purchase_medicine_HSN = models.CharField(max_length=50)
    purchase_medicine_Name = models.CharField(max_length=50)
    purchase_medicine_MFG = models.CharField(max_length=50)
    purchase_medicine_Unit = models.CharField(max_length=50)
    purchase_medicine_QTY = models.IntegerField()
    purchase_medicine_Sch = models.CharField(max_length=50)
    purchase_medicine_Batch = models.CharField(max_length=50)
    purchase_medicine_Expiry = models.CharField(max_length=50)
    purchase_medicine_M_R_P = models.CharField(max_length=50)
    purchase_medicine_Rate = models.CharField(max_length=50)
    purchase_medicine_Disc = models.CharField(max_length=50)
    purchase_medicine_Gst = models.CharField(max_length=50)
    purchase_medicine_Gst_amt = models.CharField(max_length=50)
    purchase_medicine_Amount = models.CharField(max_length=50)

    def __str__(self):
        return self.purchase_medicine_Name

class Purchase_Medicine_bill_details(models.Model):
    purchase_user_medicine_bill_token = models.IntegerField()
    purchase_medicine_bill_token = models.IntegerField()
    purchase_medicine_bill_HSN = models.CharField(max_length=50)
    purchase_medicine_bill_Name = models.CharField(max_length=50)
    purchase_medicine_bill_MFG = models.CharField(max_length=50)
    purchase_medicine_bill_Unit = models.CharField(max_length=50)
    purchase_medicine_bill_QTY = models.CharField(max_length=50)
    purchase_medicine_bill_Sch = models.CharField(max_length=50)
    purchase_medicine_bill_Batch = models.CharField(max_length=50)
    purchase_medicine_bill_Expiry = models.CharField(max_length=50)
    purchase_medicine_bill_M_R_P = models.CharField(max_length=50)
    purchase_medicine_bill_Rate = models.CharField(max_length=50)
    purchase_medicine_bill_Disc = models.CharField(max_length=50)
    purchase_medicine_bill_Gst = models.CharField(max_length=50)
    purchase_medicine_bill_Gst_amt = models.CharField(max_length=50)
    purchase_medicine_bill_Amount = models.CharField(max_length=50)

    def __str__(self):
        return self.purchase_medicine_bill_Name


class sell_medicine_details(models.Model):
    sell_medicine_user_token = models.IntegerField()
    sell_medicine_token_bill = models.IntegerField()
    sell_meicine_id = models.CharField(max_length=50)
    sell_medicine_name = models.CharField(max_length=50)
    sell_medicine_quantity = models.CharField(max_length=50)
    sell_medicine_amount = models.CharField(max_length=50)







class sell_medicine_bills(models.Model):
    sell_medicine_bill_user_token = models.IntegerField()
    sell_medicine_bill_token = models.IntegerField()
    sell_medicine_bill_Dr = models.CharField(max_length=50)
    sell_medicine_bill_patient = models.CharField(max_length=50)
    sell_medicine_bill_day = models.CharField(max_length=50)
    sell_medicine_bill_amount = models.CharField(max_length=50)


