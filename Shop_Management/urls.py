from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from Shop_Management import views

urlpatterns = [
    # Login site 
 path("",views.Login,name='Login'),
 path("Login",views.Login,name='Login'),
 path("Account",views.Account,name='Account'),
 
 #Shop site
 path("ShopHome",views.ShopHome,name='ShopHome'),

 path("Sell_Medicine",views.Sell_Medicine,name='Sell_Medicine'),
 path("sell_medicin_all_process",views.sell_medicin_all_process,name='sell_medicin_all_process'),
 path("Sell_Medicine_History",views.Sell_Medicine_History,name='Sell_Medicine_History'),

 path("Order_Medicine",views.Order_Medicine,name='Order_Medicine'),
 path("Order_History",views.Order_History,name='Order_History'),
 path("deletemedicine/<int:id>",views.deletemedicine,name='deletemedicine'),

 path("All_Medicine",views.All_Medicine,name='All_Medicine'), 
 path("Expiry_Medicine",views.Expiry_Medicine,name='Expiry_Medicine'), 
 path("No_Sell",views.No_Sell,name='No_Sell'), 

 path("Purchase_Medicine",views.Purchase_Medicine,name='Purchase_Medicine'),

 path("Purchase_Medicine_History",views.Purchase_Medicine_History,name='Purchase_Medicine_History'),

 path("Profit",views.Profit,name='Profit'),


 
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
