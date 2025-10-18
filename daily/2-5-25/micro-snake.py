import pygame as P;from random import randint as R;s=[P.Vector2(0,0)]*4;d=P.Vector2(1,0);K={P.K_DOWN:P.Vector2(0,1),P.K_UP:P.Vector2(0,-1),P.K_LEFT:P.Vector2(-1,0),P.K_RIGHT:P.Vector2(1,0)};r=10;A=0xFF0000;S=P.Color("#00FF00");a=(R(0,r-1),R(0,r-1));C=P.Surface((r,r));W=P.display.set_mode((r*50,r*50));C=P.Surface((r,r));l=0;q=0;G=P.time.Clock();J=0;N=C.get_at;n=C.set_at;V=500
while 1:
 C.fill(0)
 for event in P.event.get():
  if event.type==P.KEYDOWN:
   if d*-1!=K[event.key]and~J:d=K[event.key];J=1
 if q==0:
  n(a,A);x=0;s.append(s[-1]+d);k=s[-1]
  try:N(k)
  except:q=1;continue
  if N(k).r==0:s.pop(0)
  else:l+=1;a=(R(0,r-1),R(0,r-1))
  for i in s[:-1]:n(i,S.lerp("#000F00",x/len(s)));x+=1
  if N(k).g!=0:q=1
  n(k,S)
 else:print(l)
 W.blit(P.transform.scale(C,(V,V)));P.display.update();J=0;G.tick(9)