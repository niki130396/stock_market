from django.urls import path, include
from visualisations import views

urlpatterns = [
    path('returns_graph/', views.StockReturnsGraph.as_view(), name='returns_graph'),
    path('financials_bar_plot/', views.FinancialStatementBarPlot.as_view(), name='financials_bar_plot'),
    path('financials_graph/', views.FinancialStatementGraph.as_view(), name='financials_graph'),
    path('', views.StockPriceGraph.as_view(), name='stock_prices')
]