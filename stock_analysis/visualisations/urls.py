from django.urls import path, include
from visualisations import views

urlpatterns = [
    path('stocks/<str:symbol>/', views.ListStocks.as_view(), name='stock_prices'),
    path('stocks/returns', views.ListStockReturns.as_view(), name='stock_returns'),
    path('returns_graph/', views.StockReturnsGraph.as_view(), name='returns_graph'),
    path('financials/<str:symbol>/', views.SingleFinancialStatementView.as_view(), name='financials_data'),
    path('financials_bar_plot/', views.FinancialStatementBarPlot.as_view(), name='financials_bar_plot'),
    path('financials_graph/', views.FinancialStatementGraph.as_view(), name='financials_graph'),
    path('statement/<str:type>/', views.FinancialStatementTTMView.as_view(), name='statement_type'),
    path('statement/<str:type>/<str:sector>/', views.FinancialStatementBySector.as_view(), name='statement_type_by_sector'),
    path('financials/<int:revenue>', views.CompaniesByRevenue.as_view(), name='companies_by_revenue'),
    path('', views.StockPriceGraph.as_view(), name='home')
]