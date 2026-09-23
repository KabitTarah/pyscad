from pyscad.sign_gen.bases.sign_rectangle_arch import SignRectangleArch
from pythonscad import show

rect = SignRectangleArch()

rect.build()
show(rect.base)
show(rect.border)