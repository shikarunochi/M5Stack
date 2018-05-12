from m5stack import lcd
from retroPCCG import RetroPCCG
import gc
import uos

uos.mountsd()
lcd.clear(lcd.WHITE)

retroPCCGObj = RetroPCCG()

retroPCCGObj.executePaint("/sd/test.dat")

del retroPCCGObj
gc.collect()
