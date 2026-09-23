from pythonscad import cylinder

def magnet(d=6, t=2, tol=0.5):
    return(cylinder(t, d=d+tol))
