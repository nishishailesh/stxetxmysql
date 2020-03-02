#!/usr/bin/python3
while True:
  try:
    x=input()
    print(float(x))
  except ValueError as e:
    print (1,e)
  except Exception as e:
    print (e)
