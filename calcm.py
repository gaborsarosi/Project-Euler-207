def calcm(a,b):
    #Check the t=1 edge case:
    if b*(1)<=(2**(2)-1)*a:
      t=1
    else:
    #Binary search for t
      tl,tr=2,70
      while tl<tr-1:
          t=(tl+tr)//2
          if b*(t-1)>=(2**t-1)*a and b*(t)<(2**(t+1)-1)*a:
              break
          if b*(t-1)>(2**t-1)*a:
              tl=t
          else:
              tr=t
    
    #Write the candidate solution, given t
    ncand=1+b*t//a+1
    
    #Check if ncand moved to the next branch; if yes, move to the next branch
    while ncand>=2**(t+1):
        t+=1
        ncand=1+b*t//a+1
        
    #recover m from n
    m=ncand**2-ncand
    return m
