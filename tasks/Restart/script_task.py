# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey


from tasks.Restart.config_scheduler import Scheduler
from tasks.Restart.login import LoginHandler
from tasks.Restart.assets import RestartAssets
from tasks.base_task import BaseTask, Time
from datetime import datetime, time

from module.logger import logger
from module.exception import TaskEnd, RequestHumanTakeover




class ScriptTask(LoginHandler):

    def run(self) -> None:
        """
        主要就是登录的模块
        :return:
        """
        self.app_restart()
        raise TaskEnd('ScriptTask end')


    def app_stop(self):
        logger.hr('App stop')
        self.device.app_stop()

    def app_start(self):
        logger.hr('App start')
        self.device.app_start()
        self.app_handle_login()
        # self.ensure_no_unfinished_campaign()

    def app_restart(self):
        logger.hr('App restart')
        self.device.app_stop()
        self.device.app_start()
        self.app_handle_login()

        # self.config.task_delay(server_update=True)
        self.set_next_run(task='Restart', success=True, finish=True, server=True)
        # 如果启用了定时领体力（每天 12-14、20-22 时内各有 20 体力）
        if self.config.restart.harvest_config.enable_ap:
            now = datetime.now()
            # 如果时间在00:00-12:00之间则设定时间为当日 12 时
            if now.time() < time(12, 0):
                self.custom_next_run(task='Restart', custom_time=Time(12, 0), time_delta=0)
            # 如果时间在12:00-20:00之间则设定时间为当日 20 时
            elif now.time() >= time(12, 0) and now.time() < time(20, 0):
                self.custom_next_run(task='Restart', custom_time=Time(20, 0), time_delta=0)
            # 如果时间在20:00-23:59之间则设定时间为次日 12 时
            else:
                self.custom_next_run(task='Restart', custom_time=Time(12, 0), time_delta=1)



if __name__ == '__main__':
    from module.config.config import Config
    from module.device.device import Device

    config = Config('oas1')
    device = Device(config)
    task = ScriptTask(config, device)
    task.app_restart()
    # task.screenshot()
    # print(task.appear_then_click(task.I_LOGIN_SCROOLL_CLOSE, threshold=0.9))








