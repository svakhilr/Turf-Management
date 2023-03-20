from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('User must have an e-mail address')
        
        

        user = self.model(
            email       = self.normalize_email(email),
            
            first_name  = first_name,
            last_name   = last_name,
        )

        #password will be hashed in database
        user.set_password(password)
        user.save(using=self._db)
        return user

     #to create/Register superuser
    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            email      = self.normalize_email(email),
            
            password   = password,
            first_name = first_name,
            last_name  = last_name,
        )
        
        user.is_admin   = True
        user.is_active  = True
        user.is_staff   = True
        user.is_superadmin  = True
        user.role= "ADMIN"
        user.save(using=self._db)
        return user


class Accounts(AbstractBaseUser):
    
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        VENDOR = "VENDOR", "Vendor"

    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    role            = models.CharField(max_length=50, choices=Roles.choices)

    
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    =models.CharField(max_length=12)
    
    #Required fields
    date_joined     = models.DateField(auto_now_add=True)  
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False) 
    
    is_verified     = models.BooleanField(default=False)





    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = ['first_name', 'last_name']

    objects = MyAccountManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None): 
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class UserProfile(models.Model):
    user=models.OneToOneField(Accounts,null=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/',default='default.jpg')
    address = models.TextField(max_length=100)


    def __str__(self):
        full_name= self.user.first_name+self.user.last_name
        return full_name

class VendorProfile(models.Model):
    user=models.OneToOneField(Accounts,null=True,blank=True,on_delete=models.CASCADE)
    vendor_profile= models.ImageField(upload_to='vendor_pic',default='default.jpg')
    address1 = models.CharField(max_length=250, blank=True)
    
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    account_name = models.CharField(max_length=20, blank=True)
    document = models.FileField(upload_to="doc/", blank=True)
    approved = models.BooleanField(default=False)
    razorpay_id = models.CharField(max_length = 25, blank= True)

    def __str__(self):
        full_name= self.user.first_name+self.user.last_name
        return full_name