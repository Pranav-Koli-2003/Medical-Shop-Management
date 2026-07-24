from django.shortcuts import render

# Create your views here.
from django.shortcuts import render , redirect
from dateutil.relativedelta import relativedelta
from .models import *
from datetime import datetime , timedelta 
from django.db.models import Sum
import json
from django.http import JsonResponse
from django.core.serializers import serialize


# Create your views here.

# Login Page Star 
def Login(request):
    if request.method == "POST":
       userId = request.POST.get("userId")
       password = request.POST.get("password")
       user = User.objects.filter(userID=userId,password=password)
       if user:
           sub = User.objects.filter(userID=userId)
           for s in sub:
              request.session['Token'] = s.usertokenId
              request.session['UserName'] = s.username
              Start = s.startDate
              End = s.endDate
              if Start < End :
                  return redirect('/ShopHome')
              else:
                  return render(request,'Login.html',{'error':'Your Subscription Has Expired'})
           
       else:
           return render(request,'Login.html',{'error':'Invalid User Id & Password'})
    return render(request,'Login.html')

def Account(request):
    index = User.objects.count()
    
    # Get today's date as a date object
    today = datetime.now().date()
    
    # Add 7 days for end date
    end_date = today + timedelta(days=7)
    
    if request.method == "POST":
        usertokenId = index + 1
        userId = request.POST.get("userId")
        password = request.POST.get("password")
        userName = request.POST.get("userName")
        email = request.POST.get("email")
        mobileNo = request.POST.get("mobileNo")
        shopName = request.POST.get("shopName")
        address = request.POST.get("address")
        
        # Use proper date objects
        startDate = today
        endDate = end_date

        # Create User object
        Data = User(
            usertokenId=usertokenId,
            userID=userId,
            password=password,
            username=userName,
            email=email,
            mobile=mobileNo,
            shopName=shopName,
            address=address,
            startDate=startDate,
            endDate=endDate
        )
        Data.save()
        return redirect('Login')
    
    else:
        return render(request, 'CreateAccount.html')



#Shop Site 
def Nbar(request):
    id = request.session.get('Token')
    if not id:
        return redirect('Login')
    else:
      userData = User.objects.filter(usertokenId = id)
      data={
        'userData':userData
       }
      return render(request,'Shop/Nbar.html',{userData:'userData'})


def ShopHome(request):
    User_id = request.session.get('Token')
    if not User_id:
        return redirect('Login')

    # Fetch user data
    userData = User.objects.filter(usertokenId=User_id)
    endusersub = None
    for edu in userData:
        endusersub = edu.endDate

    # Current date
    current_date = datetime.now().date()

    # Dates for future months
    datemonth3 = current_date + relativedelta(months=3)
    datemonth6 = current_date + relativedelta(months=6)
    datemonth8 = current_date + relativedelta(months=8)

    # Medicines expiring in different ranges
    expired_medicines = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=User_id,
        purchase_medicine_Expiry__lt=current_date,
        purchase_medicine_QTY__gt=0
    ).count()

    month3_expired_medicines = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=User_id,
        purchase_medicine_Expiry__range=[current_date, datemonth3],
        purchase_medicine_QTY__gt=0
    ).count()

    month6_expired_medicines = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=User_id,
        purchase_medicine_Expiry__range=[datemonth3, datemonth6],
        purchase_medicine_QTY__gt=0
    ).count()

    month8_expired_medicines = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=User_id,
        purchase_medicine_Expiry__range=[datemonth6, datemonth8],
        purchase_medicine_QTY__gt=0
    ).count()

    # Orders with 0 quantity
    order = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=User_id,
        purchase_medicine_QTY=0
    ).count()

    # Calculate total profit safely
    total_profit = 0
    profit_bills = sell_medicine_bills.objects.filter(
        sell_medicine_bill_user_token=User_id
    )

    for bill in profit_bills:
        medicines = sell_medicine_details.objects.filter(
            sell_medicine_user_token=User_id,
            sell_medicine_token_bill=bill.sell_medicine_bill_token
        )
        for med in medicines:
            purchase_items = Purchase_Medicine_data.objects.filter(
                purchase_user_medicine_token=User_id,
                id=med.sell_meicine_id
            )
            for item in purchase_items:
                try:
                    m_r_p = float(str(item.purchase_medicine_M_R_P).replace(',', '').strip())
                except:
                    m_r_p = 0
                try:
                    rate = float(str(item.purchase_medicine_Rate).replace(',', '').strip())
                except:
                    rate = 0
                try:
                    qty = float(str(med.sell_medicine_quantity).replace(',', '').strip())
                except:
                    qty = 0

                total_rate_sell_profit = m_r_p - rate
                total_profit += total_rate_sell_profit * qty

    # Current month for display
    display_month = datetime.now().strftime("%Y-%m")

    # Prepare data for template
    data = {
        'userData': userData,
        'expired_medicines': expired_medicines,
        'month3_expired_medicines': month3_expired_medicines,
        'month6_expired_medicines': month6_expired_medicines,
        'month8_expired_medicines': month8_expired_medicines,
        'order': order,
        'total_profit': total_profit,
        'display_month': display_month,
        'endusersub': endusersub
    }

    return render(request, 'Shop/ShopHome.html', data)
    


def Sell_Medicine(request):
    id = request.session.get('Token')
    if not id:
        return redirect('Login')

    # Fetch user and sell data
    userData = User.objects.filter(usertokenId=id)
    sell = Purchase_Medicine_data.objects.filter(purchase_user_medicine_token=id ,  purchase_medicine_QTY__gt = 0,)

    # Serialize the queryset to JSON-compatible data
    sell_serialized = serialize('json', sell) # Converts to JSON-like Python objects
    
    data = {
        'userData': userData,
        'sell': sell  # Pass the serialized JSON
    }
    return render(request, 'Shop/Sell_Medicine.html', data)




def sell_medicin_all_process(request):
    # Retrieve user token from session
    user_id = request.session.get('Token')
    if not user_id:
        return redirect('login')  # Redirect to login page if Token is not found

    # Fetch user data
    userData = User.objects.filter(usertokenId=user_id)
    
    sell = Purchase_Medicine_data.objects.filter(purchase_user_medicine_token=user_id, purchase_medicine_QTY__gt = 0,)
    # Serialize the queryset to JSON-compatible data
    

    if request.method == 'POST':
        current_date = datetime.now().date()

        drname = request.POST.get('DrName')
        patientName = request.POST.get('PatientName')

        # Generate new bill ID
        bill_id = sell_medicine_bills.objects.count() + 1
        total_amount = request.POST.get('total_amount_bill')
        newbill = sell_medicine_bills(
            sell_medicine_bill_user_token=user_id,
            sell_medicine_bill_token=bill_id,
            sell_medicine_bill_Dr = drname,
            sell_medicine_bill_patient = patientName,
            sell_medicine_bill_day=current_date,
            sell_medicine_bill_amount = total_amount,
        )
        newbill.save()

        # Fetch data from POST request
        count = request.POST.getlist('count')
        medicine_id = request.POST.getlist('medicine_id')
        medicine = request.POST.getlist('medicine')
        sell_quantity = request.POST.getlist('Sell_quantity')
        sell_amount = request.POST.getlist('Sell_amount')

        # Save each medicine detail
        for i in range(len(count)):
            sell_medicine = sell_medicine_details(
                sell_medicine_user_token=user_id,  # Use `user_id` instead of `id`
                sell_medicine_token_bill=bill_id,
                sell_meicine_id=medicine_id[i],  # Corrected typo
                sell_medicine_name=medicine[i],
                sell_medicine_quantity = sell_quantity[i],
                sell_medicine_amount=sell_amount[i],
            )
            sell_medicine.save()
        
        for d in range(len(count)):
           sell_qty = Purchase_Medicine_data.objects.filter(purchase_user_medicine_token=user_id, id = medicine_id[d])
           print(sell_qty)
           for s in sell_qty:
              new_qty = int(s.purchase_medicine_QTY) - int(sell_quantity[d])
              print(new_qty) 
              s.purchase_medicine_QTY = new_qty
              print(new_qty)
              s.save()

    sell = Purchase_Medicine_data.objects.filter(purchase_user_medicine_token=user_id, purchase_medicine_QTY__gt = 0,)
    sell_serialized = serialize('json', sell) 
    data = {
        'userData': userData,
        'sell':sell,
    }
    return render(request, 'Shop/Sell_Medicine.html', data)  # Corrected to `render`






def Sell_Medicine_History(request):
    user_id = request.session.get('Token')
    if not user_id:
        return redirect('Login')
    else:
      userData = User.objects.filter(usertokenId = user_id)
      bill_di =sell_medicine_bills.objects.filter(sell_medicine_bill_user_token = user_id)[::-1]
      sell_bill_map = []
      for bill in bill_di:
        sell_medicine = sell_medicine_details.objects.filter(sell_medicine_user_token = user_id , sell_medicine_token_bill = bill.sell_medicine_bill_token)
        sell_bill_map.append({
           'bill':bill,
           'sell_medicine':sell_medicine,
        })

      data={
        'userData':userData,
        'sell_bill_map':sell_bill_map,
       }
    return render(request,'Shop/Sell_Medicine_History.html',data)





def Order_Medicine(request):
    user_id = request.session.get('Token')
    if not user_id:
        return redirect('Login')
    else:
      userData = User.objects.filter(usertokenId = user_id)
      order = Purchase_Medicine_data.objects.filter(purchase_user_medicine_token = user_id, purchase_medicine_QTY = 0,)
      data={
        'userData':userData,
        'order':order,
       }
    return render(request,'Shop/Order_Medicine.html',data)


def deletemedicine(request,id):
 post = Purchase_Medicine_data.objects.filter(id=id)
 post.delete()
 return redirect('/Order_Medicine')




def Order_History(request):
    id = request.session.get('Token')
    if not id:
        return redirect('Login')
    else:
      userData = User.objects.filter(usertokenId = id)
      data={
        'userData':userData
       }
    return render(request,'Shop/Order_History.html',data)


def Expiry_Medicine(request):
    id = request.session.get('Token')
    
    if not id:
        return redirect('Login')

    # Get user data
    userData = User.objects.filter(usertokenId=id)

    # Get the current date
    current_date = datetime.now().date()

    # Calculate dates for 8 months and 12 months ahead
    datemonth3 = current_date + relativedelta(months=3)
    datemonth6 = current_date + relativedelta(months=6)
    datemonth8 = current_date + relativedelta(months=8)

    # Medicines expiring within 8 months
    expired_medicines = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=id,
        purchase_medicine_Expiry__lt=current_date,
         purchase_medicine_QTY__gt = 0,
    )

    # Medicines expiring within 12 months
    month3_expired_medicines = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=id,
        purchase_medicine_Expiry__range=[current_date, datemonth3],
         purchase_medicine_QTY__gt = 0,
    )

    # Medicines expiring within 12 months
    month6_expired_medicines = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=id,
        purchase_medicine_Expiry__range=[datemonth3, datemonth6],
         purchase_medicine_QTY__gt = 0,
    )

    # Medicines expiring within 12 months
    month8_expired_medicines = Purchase_Medicine_data.objects.filter(
        purchase_user_medicine_token=id,
        purchase_medicine_Expiry__range=[datemonth6, datemonth8],
         purchase_medicine_QTY__gt = 0,
    )

    # Pass data to the template
    data = {
        'userData': userData,
        'expired_medicines': expired_medicines,
        'month3_expired_medicines': month3_expired_medicines,
        'month6_expired_medicines': month6_expired_medicines,
        'month8_expired_medicines': month8_expired_medicines
    }

    return render(request, 'Shop/Expiry_Medicine.html', data)





def All_Medicine(request):
    id = request.session.get('Token')
    if not id:
        return redirect('Login')
    else:
      userData = User.objects.filter(usertokenId = id)
      medicine_all = Purchase_Medicine_data.objects.filter(purchase_user_medicine_token = id , purchase_medicine_QTY__gt = 0,)
      data={
        'userData':userData,
        'medicine_all':medicine_all
       }
    return render(request,'Shop/All_Medicine.html',data)


def No_Sell(request):
    id = request.session.get('Token')
    if not id:
        return redirect('Login')
    else:
      userData = User.objects.filter(usertokenId = id)
      data={
        'userData':userData
       }
    return render(request,'Shop/No_Sell.html',data)




def Purchase_Medicine(request):
    id = request.session.get('Token')
    
    purchase_id = Purchase_Company.objects.count() + 1
    
    if not id:
        return redirect('Login')
    else:
      userData = User.objects.filter(usertokenId = id)
      company_info = Purchase_Company.objects.filter(purchase_user_company_token = id)

      if request.method =='POST':
        company = request.POST.get('company')
        address = request.POST.get('company_address')
        phone = request.POST.get('phone')
        state_code = request.POST.get('state_code')
        gstin = request.POST.get('gstin')
        pan = request.POST.get('pan')
        Company_DL_No = request.POST.get('DL_No')
        invoice_no = request.POST.get('invoice_no')
        date = request.POST.get('date')
        Dul_bal = request.POST.get('Dul_bal')
        POno = request.POST.get('POno')
        salesman = request.POST.get('salesman')
        Gross = request.POST.get('Gross')
        purchase_CGST = request.POST.get('CGST')
        purchase_CGST_Taxable = request.POST.get('CGST_Taxable')
        purchase_CGST_TaxAmt = request.POST.get('CGST_TaxAmt')
        purchase_SGST = request.POST.get('SGST')
        purchase_SGST_Taxable = request.POST.get('SGST_Taxable')
        purchase_SGST_TaxAmt = request.POST.get('SGST_TaxAmt')
        purchase_Total_GST = request.POST.get('Total_GST')
        purchase_Total_Disc = request.POST.get('Total_Disc')
        purchase_Less = request.POST.get('Less')
        purchase_Add = request.POST.get('Add')
        purchase_NET = request.POST.get('NET')

        purchaseData = Purchase_Company(
           purchase_user_company_token = id,
           purchase_compnay_token = purchase_id,
           purchase_compnay_name = company,
           purchase_compnay_address = address,
           purchase_compnay_phone = phone,
           purchase_compnay_state_code = state_code,
           purchase_compnay_gstin = gstin,
           purchase_compnay_pan = pan,
           purchase_compnay_DL_no = Company_DL_No,
           purchase_invoice_no = invoice_no,
           purchase_date = date,
           purchase_Dul_bal = Dul_bal,
           purchase_POno = POno,
           purchase_salesman = salesman,
           purchase_Gross = Gross,
           purchase_CGST = purchase_CGST,
           purchase_CGST_Taxable = purchase_CGST_Taxable,
           purchase_CGST_TaxAmt = purchase_CGST_TaxAmt,
           purchase_SGST = purchase_SGST,
           purchase_SGST_Taxable = purchase_SGST_Taxable,
           purchase_SGST_TaxAmt = purchase_SGST_TaxAmt,
           purchase_Total_GST = purchase_Total_GST,
           purchase_Total_Disc = purchase_Total_Disc,
           purchase_Less = purchase_Less,
           purchase_Add = purchase_Add,
           purchase_NET = purchase_NET,
        )
        
        purchaseData.save()

        medicine_HSN = request.POST.getlist('medicine_HSN')
        medicine_Name = request.POST.getlist('medicine_Name')
        medicine_MFG = request.POST.getlist('medicine_MFG')
        medicine_Unit = request.POST.getlist('medicine_Unit')
        medicine_QTY = request.POST.getlist('medicine_QTY')
        medicine_Sch = request.POST.getlist('medicine_Sch')
        medicine_Batch = request.POST.getlist('medicine_Batch')
        medicine_Expiry = request.POST.getlist('medicine_Expiry')
        medicine_M_R_P = request.POST.getlist('medicine_M_R_P')
        medicine_Rate = request.POST.getlist('medicine_Rate')
        medicine_Disc = request.POST.getlist('medicine_Disc')
        medicine_Gst = request.POST.getlist('medicine_Gst')
        medicine_Gst_amt = request.POST.getlist('medicine_Gst_amt')
        medicine_Amount = request.POST.getlist('medicine_Amount')

        
        
        for i in range(len(medicine_HSN)):
          medicindata = Purchase_Medicine_data(
             purchase_user_medicine_token = id,
             purchase_medicine_token = purchase_id,
             purchase_medicine_HSN = medicine_HSN[i],
             purchase_medicine_Name = medicine_Name[i],
             purchase_medicine_MFG = medicine_MFG[i],
             purchase_medicine_Unit = medicine_Unit[i],
             purchase_medicine_QTY = medicine_QTY[i],
             purchase_medicine_Sch = medicine_Sch[i],
             purchase_medicine_Batch = medicine_Batch[i],
             purchase_medicine_Expiry = medicine_Expiry[i],
             purchase_medicine_M_R_P = medicine_M_R_P[i],
             purchase_medicine_Rate = medicine_Rate[i],
             purchase_medicine_Disc = medicine_Disc[i],
             purchase_medicine_Gst = medicine_Gst[i],
             purchase_medicine_Gst_amt = medicine_Gst_amt[i],
             purchase_medicine_Amount = medicine_Amount[i],
          ) 
          medicindata.save()
        
        
        for i in range(len(medicine_HSN)):
          medicine_details = Purchase_Medicine_bill_details(
             purchase_user_medicine_bill_token = id,
             purchase_medicine_bill_token = purchase_id,
             purchase_medicine_bill_HSN = medicine_HSN[i],
             purchase_medicine_bill_Name = medicine_Name[i],
             purchase_medicine_bill_MFG = medicine_MFG[i],
             purchase_medicine_bill_Unit = medicine_Unit[i],
             purchase_medicine_bill_QTY = medicine_QTY[i],
             purchase_medicine_bill_Sch = medicine_Sch[i],
             purchase_medicine_bill_Batch = medicine_Batch[i],
             purchase_medicine_bill_Expiry = medicine_Expiry[i],
             purchase_medicine_bill_M_R_P = medicine_M_R_P[i],
             purchase_medicine_bill_Rate = medicine_Rate[i],
             purchase_medicine_bill_Disc = medicine_Disc[i],
             purchase_medicine_bill_Gst = medicine_Gst[i],
             purchase_medicine_bill_Gst_amt = medicine_Gst_amt[i],
             purchase_medicine_bill_Amount = medicine_Amount[i],
          ) 
          medicine_details.save()
      company_info = Purchase_Company.objects.filter(purchase_user_company_token = id)
      company_info_serialized = serialize('json',company_info)
      data={
        'userData':userData,
        'company_info':company_info,
       }
    return render(request,'Shop/Purchase_Medicine.html',data)




def Purchase_Medicine_History(request):
    id = request.session.get('Token')
    if not id:
        return redirect('Login')

    # Fetch user and company data
    userData = User.objects.filter(usertokenId=id)
    companies = Purchase_Company.objects.filter(purchase_user_company_token=id)
    
    # Build company-medicine mapping
    company_medicine_map = []
    for company in companies:
        medicines = Purchase_Medicine_bill_details.objects.filter(
            purchase_user_medicine_bill_token=id,
            purchase_medicine_bill_token=company.purchase_compnay_token
        )
        
        company_medicine_map.append({
            'company': company,
            'medicines': medicines
        })
    
    # Pass data to the template
    data = {
        'userData': userData,
        'company_medicine_map': company_medicine_map,
    }
    return render(request, 'Shop/Purchase_Medicine_History.html', data)



def Profit(request):
    user = request.session.get('Token')
    if not user:
        return redirect('Login')

    period = request.GET.get("period", "1m")
    userData = User.objects.filter(usertokenId=user)

    today = datetime.today().date()

    if period == "1m":
        start_date = today - timedelta(days=30)
    elif period == "3m":
        start_date = today - timedelta(days=90)
    elif period == "6m":
        start_date = today - timedelta(days=180)
    else:
        start_date = today - timedelta(days=30)

    # --------------------------
    # FIX 1: Convert string NET to float manually
    # --------------------------
    purchases = Purchase_Company.objects.filter(
        purchase_date__range=[start_date, today]
    )

    purchase_total = 0
    for p in purchases:
        try:
            purchase_total += float(p.purchase_NET)
        except:
            purchase_total += 0

    # --------------------------
    # FIX 2 & 3: Convert sell amount manually
    # --------------------------
    sells = sell_medicine_bills.objects.all()
    sell_total = 0

    for s in sells:
        try:
            sell_date = datetime.strptime(s.sell_medicine_bill_day, "%Y-%m-%d").date()

            if start_date <= sell_date <= today:
                sell_total += float(s.sell_medicine_bill_amount)
        except:
            pass

    # --------------------------
    # PROFIT
    # --------------------------
    profit = sell_total - purchase_total

    context = {
        "profit": profit,
        "sell_total": sell_total,
        "purchase_total": purchase_total,
        "period": period,
        'userData':userData,

    }
    return render(request, 'Shop/Profit.html', context)
