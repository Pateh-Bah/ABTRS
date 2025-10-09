from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.BookingListView.as_view(), name="list"),
    path("create/", views.BookingCreateView.as_view(), name="create"),
    path("search/", views.BookingSearchView.as_view(), name="search"),
    path("payment/<int:pk>/", views.PaymentView.as_view(), name="payment"),
    path(
        "payment-success/<int:pk>/",
        views.PaymentSuccessView.as_view(),
        name="payment_success",
    ),
    path("ticket/<int:pk>/", views.TicketView.as_view(), name="ticket"),
    path("ticket/<int:pk>/pdf/", views.TicketPDFView.as_view(), name="ticket_pdf"),
    path(
        "ajax/get-seat-availability/",
        views.get_seat_availability,
        name="ajax_get_seat_availability",
    ),
    path(
        "ajax/get-route-buses/",
        views.get_route_buses_ajax,
        name="ajax_get_route_buses",
    ),
    path(
        "bus-seats/",
        views.get_seat_availability,
        name="bus_seats",
    ),
    path("debug/", views.BookingDebugView.as_view(), name="debug"),
    path('track/<str:pnr_code>/', views.track_booking_by_pnr, name='track_booking_by_pnr'),

]