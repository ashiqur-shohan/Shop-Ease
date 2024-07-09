from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,username,email,password, **extra_fields):
        if not username:
            raise ValueError('Username is required.')
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        
        #user create kortesi 
        user = self.model(
            username = username,
            email = email,
            **extra_fields
        )
        user.set_password(password)
        #'using=self._db' eita na dile o hbe. ekhane bole dicchi je default database a save korte
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        #'using=self._db' eita na dile o hbe. ekhane bole dicchi je default database a save korte
        user.save(using=self._db)
        return user
