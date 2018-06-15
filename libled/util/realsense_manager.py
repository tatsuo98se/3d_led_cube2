import logger
class RealsenseManager:
    pass

try:
    import pyrealsense as pyrs
    import realsense_manager_impl
    RealsenseManager = realsense_manager_impl.RealsenseManager
except:
    logger.w("librealsense is not installed.")
    import realsense_manager_dummy
    RealsenseManager = realsense_manager_dummy.RealsenseManager
