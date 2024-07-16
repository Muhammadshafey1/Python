# PASSWORD GENERATOR
import random
import string

lenght = int(input('ENTER YOUR PASSWORD LENGHT:'))

lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
symbols = string.punctuation

all = lower + upper + num +symbols

temp = random.sample(all, lenght)

password = "".join(temp)
output =(f"Your password is: {password}")
print(output)