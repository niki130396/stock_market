from django.urls import path, include
from api import views

urlpatterns = [
    path('stocks/<str:symbol>/', views.ListStocks.as_view(), name='stock_prices_api'),
    path('stocks/returns', views.ListStockReturns.as_view(), name='stock_returns_api'),
    path('financials/<str:symbol>/', views.SingleFinancialStatementView.as_view(), name='financials_data'),
    path('statement/<str:type>/', views.FinancialStatementTTMView.as_view(), name='statement_type'),
    path('statement/<str:type>/<str:sector>/', views.FinancialStatementBySector.as_view(), name='statement_type_by_sector'),
    path('financials/<int:revenue>', views.CompaniesByRevenue.as_view(), name='companies_by_revenue'),
]
