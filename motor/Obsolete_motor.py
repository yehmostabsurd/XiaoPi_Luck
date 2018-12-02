from rrb2 import *
rr = RRB2()

keyin = True
while(keyin):
    keyin = raw_input("Please make me happy......  ")
    if keyin == "forward":
        rr.forward(5)
        keyin = True
    if keyin == "reverse":
        rr.reverse(5)
        keyin = True
    if keyin == "right":
        rr.right(5)
        keyin = True
    if keyin == "quit":
        keyin = False
    else:
        keyin = True
        

