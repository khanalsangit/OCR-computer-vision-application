import asyncio
import torch

async def gpu_task():
    while True:
        # Perform GPU computation here
        tensor = torch.rand(10000, 10000, device='cuda')
        result = tensor.mean()
        
        await asyncio.sleep(1)  # Wait for 1 second before the next iteration

async def main():
    tasks = [gpu_task() for _ in range(2)]  # Start multiple GPU tasks
    
    # Run the tasks concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
