from django.urls import path, include
from api import views

urlpatterns = [
    path('stocks/<str:symbol>/', views.StockPriceLister.as_view(), name='stock_prices_api'),
    path('stocks/returns', views.ListStockReturns.as_view(), name='stock_returns_api'),
    path('financials/<str:symbol>/', views.SingleFinancialStatementView.as_view(), name='financials_data'),
    path('statement/', views.FilteredStatementsView.as_view(), name='statement_type'),
    path('financials/<int:revenue>', views.CompaniesByRevenueLister.as_view(), name='companies_by_revenue')
]
