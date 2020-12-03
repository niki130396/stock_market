from django.urls import path

from visualisations import views

urlpatterns = [
    path('returns_graph/', views.StockReturnsGraph.as_view(), name='returns_graph'),
    path('financials_bar_plot/', views.FinancialStatementBarPlot.as_view(), name='financials_bar_plot'),
    path('financials_graph/', views.FinancialStatementGraph.as_view(), name='financials_graph'),
    path('', views.StockPriceGraph.as_view(), name='stock_prices'),
    path('area/', views.IncomeStatementKeyMetricsAreaPlot.as_view(), name='income_area'),
    path('compare/', views.CompareCompaniesView.as_view(), name='compare')
]
