from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calculate-chart/', views.calculate_chart, name='calculate_chart'),
    path('calculate-synastry/', views.calculate_synastry_view, name='calculate_synastry'),
    path('daily-planner/', views.get_daily_planner, name='daily_planner'),
    path('weekly-forecast/', views.get_weekly_forecast, name='weekly_forecast'),
    path('draw-tarot/', views.draw_tarot, name='draw_tarot'),
    path('career-analysis/', views.calculate_career_view, name='career_analysis'),
    path('rectify-time/', views.rectify_birth_time, name='rectify_time'),
    path('countries/', views.get_countries, name='get_countries'),
    path('provinces/', views.get_provinces, name='get_provinces'),
    path('cities/', views.get_cities, name='get_cities'),
    path('daily-horoscopes/', views.get_daily_horoscopes_api, name='daily_horoscopes'),
    
    # Auth
    path('auth/', views.auth_view, name='auth'),
    path('register/', views.register_api, name='register'),
    path('login/', views.login_api, name='login'),
    path('logout/', views.logout_api, name='logout'),
    path('check-auth/', views.check_auth_api, name='check_auth'),
    path('update-profile/', views.update_profile_api, name='update_profile'),
    path('custom-admin/', views.custom_admin_dashboard, name='custom_admin'),
]
