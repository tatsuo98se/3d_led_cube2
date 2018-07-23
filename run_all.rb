require "timeout"

begin
pids = [
spawn("python ./main_hw_controller_module.py"),
#spawn("python ./main_hw_controller_module_dummy.py"),
spawn("python ./main_realsense_module.py"),
spawn("python ./main_paint_service.py"),
spawn("python ./main_realsense_service.py"),
spawn("python ./main_block_service.py"),
]
end

begin
    sleep
rescue SignalException
    pids.each do |pid|
        begin
            Timeout.timeout(5) do
                puts "[INFO] aborting PID:#{pid}. waiting..."
                Process.kill("INT", pid)
                Process.wait pid
                puts "[INFO] PID:#{pid} has aborted successfully."
            end
        rescue Timeout::Error
            puts "[ERR] PID:#{pid} has not aborted. the process will be killed forcibly."
            Process.kill(:KILL, pid)
        end
    end
end
