-- Active: 1761948861399@@127.0.0.1@3306
/* 
we chose to skip this method because it is not the best way to seed the database
because of the following reasons:
there is no way to hash the passwords
if we create a user, we have to manually hash the password
and if we dont, the password either way wont work
cause unhashing will not be the same as the hashed password
eg if i put 123 as the password
the application will think, thats the password after hashing
but we dont know the reverse of the hashing algorithm
so using 123 as the password will not work
so we chose to skip this method
 */