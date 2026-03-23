'''
    tasklist | findstr [PID]  # Windows下查看进程
'''
import threading
import subprocess
import time
import os
import sys
import signal


class DaemonThreadWithSubprocess(threading.Thread):
    def __init__(self, cmd: list):
        super().__init__()
        self.cmd = cmd  # 子进程命令（推荐列表形式，避免shell注入）
        self.process = None  # 保存子进程对象
        self.daemon = True  # 设为守护线程，主进程退出时线程直接终止

    def run(self):
        """守护线程核心逻辑：启动子进程并绑定到主进程/线程"""
        # 跨平台进程组配置（确保子进程随主进程退出）
        startupinfo = None
        creationflags = 0
        preexec_fn = None

        if sys.platform == "win32":
            # Windows：创建新进程组，主进程退出时终止该组
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            # Linux/macOS：将子进程加入主进程的进程组
            preexec_fn = lambda: os.setpgid(0, 0)  # 子进程成为新进程组组长，归属主进程

        try:
            # 启动子进程
            self.process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                # Windows特有配置
                startupinfo=startupinfo,
                creationflags=creationflags,
                # Linux/macOS特有配置
                preexec_fn=preexec_fn,
                # 禁止子进程继承文件描述符（可选）
                close_fds=True if sys.platform != "win32" else None
            )
            print(f"✅ 子进程启动 | PID: {self.process.pid} | 线程ID: {threading.get_ident()}")
            
            # 等待子进程执行（守护线程退出时会中断此处）
            stdout, stderr = self.process.communicate()
            if stdout:
                print(f"📝 子进程输出: {stdout.strip()}")
            if stderr:
                print(f"❌ 子进程错误: {stderr.strip()}")

        finally:
            # 兜底：线程终止时主动清理子进程（双重保障）
            self._terminate_subprocess()

    def _terminate_subprocess(self):
        """跨平台终止子进程"""
        if not self.process or self.process.poll() is not None:
            return  # 子进程已退出
        
        try:
            if sys.platform == "win32":
                # Windows：终止进程组（/T 表示终止子进程及其子进程）
                subprocess.call(
                    ["taskkill", "/F", "/T", "/PID", str(self.process.pid)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                # Linux/macOS：终止整个进程组（SIGTERM 优雅终止，SIGKILL 强制杀死）
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                # 等待1秒，若未退出则强制杀死
                time.sleep(1)
                if self.process.poll() is None:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
            
            # 等待子进程彻底退出
            self.process.wait(timeout=2)
            print(f"🔚 子进程已终止 | PID: {self.process.pid}")
        except Exception as e:
            print(f"⚠️  终止子进程失败: {e}")


# ------------------- 测试代码 -------------------
if __name__ == "__main__":
    # 示例：启动一个长时间运行的子进程（模拟耗时任务）
    if sys.platform == "win32":
        # Windows 测试命令：每隔1秒输出一次，持续30秒
        test_cmd = ["cmd", "/c", "for /l %i in (1,1,30) do (echo 子进程运行中...%i & timeout /t 1 /nobreak)"]
    else:
        # Linux/macOS 测试命令：每隔1秒输出一次，持续30秒
        test_cmd = ["bash", "-c", "for i in {1..30}; do echo '子进程运行中...$i'; sleep 1; done"]
    
    # 启动守护线程
    thread = DaemonThreadWithSubprocess(test_cmd)
    thread.start()
    
    # 主线程运行5秒后主动退出（模拟业务逻辑完成）
    print("🔵 主线程运行中，5秒后退出...")
    time.sleep(5)
    print("🔴 主线程退出，守护线程和子进程将自动终止")
    
    # 主进程退出（无需等待守护线程，守护线程会被强制终止，子进程也会被清理）
    sys.exit(0)
