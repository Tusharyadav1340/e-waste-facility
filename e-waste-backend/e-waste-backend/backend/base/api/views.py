from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, CustomUserDetailsSerializer, CustomUserProductSerializer, CustomUserProductSellerSerializer, LoginSerializer, EducationSerializer, TransactionSerializer, FacilitySerializer, CouponSerializer, CouponRedemptionSerializer, GetCouponRedemptionSerializer
from base.models import CustomUser, UserProducts, Education, Transaction, Facility, Coupon, CouponRedemption
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_choices == 'employee'
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': str(user.user_choices),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        reg_serializer = CustomUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()  
            # print(reg_serializer.data)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        userid = request.GET.get('userid')
        queryset = CustomUser.objects.get(id=userid)
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomUserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserDetailsSerializer

    def get(self, request):
        userid = self.request.query_params.get('userid')
        try:
            user = CustomUser.objects.get(id=userid)
            serializer = CustomUserDetailsSerializer(user)
            # print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            raise Http404("User does not exist")

    def post(self, request):
        userid = request.query_params.get('userid')
        try:
            user = CustomUser.objects.get(id=userid)
            serializer = CustomUserDetailsSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            raise Http404("User does not exist")

class CustomUserProductView(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserProductSerializer

    def get(self, request):
        statusget = request.query_params.get('filter')
        print(statusget)
        userid = request.user.id
        print(userid)
        try:
            if statusget == 'empty':
                user = UserProducts.objects.filter(user=userid)
            else: 
                user = UserProducts.objects.filter(user=userid, status=statusget)
            print(user)
            serializer = CustomUserProductSerializer(user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProducts.DoesNotExist:
            raise Http404("User does not exist")

    def post(self, request):
        ewaste_coins = {
            'Phone': 100,
            'Headset': 150,
            'Laptop': 300,
            'Mixer': 200,
            'Refrigerator': 500,
            'Speaker': 250,
            'Television': 400,
            'Washing Machine': 450,
        }
        user = request.user
        user_email = request.user.email

        try:
            created_by = CustomUser.objects.get(email=user_email)
            user_product = UserProducts(user=created_by)

            product_type = request.data.get('product_type')

            if product_type in ewaste_coins:
                user_product.product_type = product_type
                user_product.coins = ewaste_coins[product_type]

            import random
            import string
            order_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            user_product.orderno = order_no
            user_product.status = 'None'

            serializer = CustomUserProductSerializer(user_product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                user.save()
                return Response({'message': 'User product created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            raise Http404("User does not exist")

class CustomUserProductSellerView(APIView):

    def get(self, request):
        
        self.permission_classes = [IsAuthenticated, IsEmployee]
        try:
            ticketid = request.query_params.get('ticketid')
            userid = request.query_params.get('id')
            print(ticketid, userid)
            try:
                user = UserProducts.objects.filter(user=userid, id=ticketid)
                print(user)
                serializer = CustomUserProductSerializer(user, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except UserProducts.DoesNotExist:
                raise Http404("User does not exist")
        except:
            pass
    
    def post(self, request):
        ticketid = request.data.get('id')
        user_id = request.data.get('user')
        seller = request.user.id
        userid = CustomUser.objects.get(id=user_id)
        sellerid = CustomUser.objects.get(id=seller)
        self.permission_classes = [IsAuthenticated, IsEmployee]

        try:
            user_product = UserProducts.objects.get(user=userid, id=ticketid)
            import random
            import string
            transaction_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            user_product.transaction_no = transaction_no
            user_product.status = 'Yes'
            coins = user_product.coins
            serializer = CustomUserProductSellerSerializer(user_product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                trans = Transaction.objects.create(user=userid, coins=coins, seller=sellerid, product=user_product, credit=True)
                user_info = CustomUser.objects.get(id=user_id)
                user_info.total_coins += coins
                user_info.total_recycle += 1
                user_info.save()
                return Response({'message': 'User product created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            raise Http404("User does not exist")
    
class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class EducationView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        try:
            if id:
                education = Education.objects.get(id=id)
                serializer = EducationSerializer(education)
            else:
                education = Education.objects.all().order_by('-created_on').values()  
                serializer = EducationSerializer(education, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Education.DoesNotExist:
            return Response({"error": "Education record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionsView(APIView):
    permission_classes = [IsAuthenticated, IsEmployee]

    def get(self, request):
        try:
            trans = Transaction.objects.filter(seller=request.user).order_by('-time')
            serializer = TransactionSerializer(trans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.decorators import api_view, permission_classes, authentication_classes

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_transactions(request):
    try:
        trans = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(trans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class FacilityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            trans = Facility.objects.all()
            serializer = FacilitySerializer(trans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = CouponSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Coupon created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            current_datetime = timezone.now()  # Get the current date and time
            
            # Update is_active status for expired coupons
            expired_coupons = Coupon.objects.filter(expiration_date__lte=current_datetime)
            expired_coupons.update(is_active=False)
            coupons = Coupon.objects.all().order_by('created_at') 
            serializer = CouponSerializer(coupons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CouponRedemptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mutable_data = request.data.copy()
        mutable_data['user'] = request.user.id
        coupon = mutable_data['coupon']
        serializer = CouponRedemptionSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            coupons = Coupon.objects.get(id=coupon)
            user = request.user
            if user.total_coins < coupons.value:
                return Response({"Failed":"Don't have enough coins"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:   
                user.total_coins -= coupons.value
                user.save()
            Transaction.objects.create(user=user, coins=coupons.value, coupon=coupons, credit=False)
            return Response({"message": "Coupon Redeemed Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        try:    
            coupons = CouponRedemption.objects.filter(user=request.user).order_by('redeemed_at')
            serializer = GetCouponRedemptionSerializer(coupons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
