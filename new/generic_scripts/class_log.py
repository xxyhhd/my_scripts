import logging

class DualLogger:
    def __init__(self, log_file, level=logging.DEBUG):
        # 创建一个logger实例
        self.logger = logging.getLogger('dual_logger')
        self.logger.setLevel(level)
        
        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        # 创建屏幕输出的handler
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(level)
        # console_handler.setFormatter(formatter)
        # self.logger.addHandler(console_handler)

        # 创建文件输出的handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        
    def debug(self, message):
        self.logger.debug(message)
        
    def info(self, message):
        self.logger.info(message)
        
    def warning(self, message):
        self.logger.warning(message)
        
    def error(self, message):
        self.logger.error(message)
        
    def critical(self, message):
        self.logger.critical(message)
