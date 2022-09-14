from django.test import TestCase
from datetime import datetime, timedelta

# Create your tests here.

now = datetime.now()
future_15days = now + timedelta(days = 15)

#print(f"Hi, {future_15days.strftime('%Y-%m-%d')}")#\

print("hi {now}")