import pygame as g,random as q
w=g.display.set_mode((99,99));R=30;r=1;y=9;v=1;c=g.time.Clock();p=[[4,10],[4,20],[4,R]];d=0;s=0;o=0;S=g.Surface((R,R));P=0;l=g.draw.line
while r:
 g.event.get()
 S.fill(99)
 if o==0:
  if g.mouse.get_just_pressed()[0]:o=1
  else:g.display.flip();continue
 if d:S.fill(0);print(s)
 else:
  for i in p:
   i[1]-=1
   if i[1]<0:
    if y>i[0]&y<i[0]+8:s+=1
    i[1]=R;i[0]=q.randint(6,20)
   l(S,P,(i[1],0),(i[1],i[0]));l(S,P,(i[1],i[0]+8),(i[1],R))
  if g.mouse.get_just_pressed()[0]:v=-3
  v+=1;y+=v
  if S.get_at((1,y)).b<5:d=1
  S.set_at((1,y),0)
 w.blit(g.transform.scale(S,(99,99)));g.display.flip();c.tick(9)
g.quit()