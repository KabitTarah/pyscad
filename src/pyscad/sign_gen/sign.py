from pyscad.sign_gen.sign_shapes import SignRectangle
from pythonscad import show

rect = SignRectangle()

rect.build()
#show(rect.base.union(rect.border))
show(rect.border)