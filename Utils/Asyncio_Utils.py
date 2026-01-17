import asyncio
import subprocess


async def simple_run_in_thread(cmd):
    print(f"正在异步运行命令: {cmd}")
    
    # 将 subprocess.run() 放在一个线程中执行
    loop_result = await asyncio.to_thread(
        subprocess.run,
        cmd,
        capture_output=True, # 捕获 stdout 和 stderr
        text=True,           # 以文本模式处理输出
        check=False          # 不要自动抛出错误
    )
    
    print("命令执行完毕。")
    print(f"Stdout: {loop_result.stdout.strip()}")
    print(f"Return Code: {loop_result.returncode}")
    
    return loop_result


async def stream_output():
    # 注意：我们必须设置 stdout=PIPE 才能获取 StreamReader
    process = await asyncio.create_subprocess_exec(
        'ping', '127.0.0.1', # Linux/macOS ping 4次
        stdout=asyncio.subprocess.PIPE, 
        stderr=asyncio.subprocess.PIPE
    )

    print("--- 实时输出 ---")
    
    # 循环读取 stdout 直到 EOF
    while True:
        # await process.stdout.readline() 会非阻塞地等待一行数据
        line = await process.stdout.readline()
        if not line:
            break
        try:
            print(f"子进程: {line.decode('gbk').strip()}")
        except UnicodeDecodeError:
            print(f"子进程: {line}")

    await process.wait() # 等待进程完全结束
    print(f"--- 进程结束，退出码: {process.returncode} ---")


if __name__ == "__main__":
    asyncio.run(simple_run_in_thread("ping 127.0.0.1"))