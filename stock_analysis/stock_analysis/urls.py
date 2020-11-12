"""stock_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from visualisations import views

urlpatterns = [
    path('admin/', admin.site.urls),
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
