
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import paypalrestsdk
from turfs.models import Booking,Booked_Timeslots,Turf
from .models import Payment






class PayPalpayment(APIView):
    
    def post(self, request):
        paypalrestsdk.configure({
            "mode": "sandbox", # sandbox or live
            "client_id": "AXW-ndd5dqgIyvZFy27ZhIqVSUzWYgxAkqLhylBmvs5TUmeONN8N62DYEVuRAWi6_SS1blmdOZEaU9l8",
            "client_secret": "ENzwTIy6whsGnsm7ZlDz1Ay3XBHwf3el4cn5YSFXCDBSNM3NjUK8Vv1W8N-UnZNgPKuMkef2Au3vzRMy" })
        
        try:
            turf_id= request.data['turf_id']
            turf = Turf.objects.get(id=turf_id)
        except:
            return Response({"message":"Turf not found"},status=status.HTTP_400_BAD_REQUEST)          

        payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"},
    "redirect_urls": {
        "return_url": "http://127.0.0.1:8000/api/payment/paypal/status/",
        "cancel_url": "https://example.com/cancel"},
    "transactions": [{
        "item_list": {
            "items": [{
                "name": "turf.name",
                "sku": "item",
                "price": "5.00",
                "currency": "USD",
                "quantity": 1}]},
        "amount": {
            "total": "5.00",
            "currency": "USD"},
        "description": "This is the payment transaction description."}]})
        
        print(payment)

        if payment.create():
          return Response({'approval_url': payment.links[1].href})
        else:
            return Response({'error': payment.error},status=status.HTTP_400_BAD_REQUEST)


class Checkout(APIView):
     def get(self, request):
        payment_id = request.data['paymentId']
        payer_id = request.data[ 'PayerID']
        print(payer_id)
        booking_number = request.data['booking_number']
        print(booking_number)
        try:
            booking = Booking.objects.get(booking_number= booking_number)

        except:
            return Response({"message":"invalid booking number"},status=status.HTTP_400_BAD_REQUEST)


        
        paypalrestsdk.configure({
            "mode": "sandbox", # sandbox or live
            "client_id": "AXW-ndd5dqgIyvZFy27ZhIqVSUzWYgxAkqLhylBmvs5TUmeONN8N62DYEVuRAWi6_SS1blmdOZEaU9l8",
            "client_secret": "ENzwTIy6whsGnsm7ZlDz1Ay3XBHwf3el4cn5YSFXCDBSNM3NjUK8Vv1W8N-UnZNgPKuMkef2Au3vzRMy" })
        
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            # Payment successful, update your database and return success response
            booking.status = "Confirmed"
            booking.save()
            Booked_Timeslots.objects.create(timeslot=booking.timeslot,booking_date=booking.date,user=booking.user,turf=booking.timeslot.turf)
            Payment.objects.create(payment_id=payment_id,booking_id=booking_number)
            return Response({'status': 'success'},status=status.HTTP_200_OK)
        else:
            # Payment failed, return error response
            return Response({'status': 'error'})
        

class PaymentResponse(APIView):
    def get(self,request):
        payment_id = request.GET.get('paymentId')
        print(payment_id)
        return Response({"message":"Payment initiated","payment_id":payment_id},status=status.HTTP_200_OK)