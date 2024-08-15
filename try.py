import subprocess

def set_gpu_power_mode(gpu_index, mode):
    command = f'nvidia-smi -i {gpu_index} -pm {mode}'
    subprocess.run(command, shell=True)

# Example usage
gpu_index = 0  # Replace with the index of your GPU
power_mode = 1  # Use 1 for "Enabled", 0 for "Disabled"

set_gpu_power_mode(gpu_index, power_mode)