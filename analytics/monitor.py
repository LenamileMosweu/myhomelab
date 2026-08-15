import os
import re
import time
import platform
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean visualization theme parameters
sns.set_theme(style="darkgrid")
timestamp_log = []
memory_usage_log = []

# Dynamically parse which server node is currently executing the script
current_node = platform.node()
print(f"🚀 Initializing Metric Monitor on Node: [{current_node}]")

# Collect 5 metric data frames across short intervals
for frame in range(5):
    with open('/proc/meminfo', 'r') as file:
        content = file.read()
        
    mem_total = int(re.search(r'MemTotal:\s+(\d+)', content).group(1))
    mem_avail = int(re.search(r'MemAvailable:\s+(\d+)', content).group(1))
    
    used_percentage = ((mem_total - mem_avail) / mem_total) * 100
    current_time = time.strftime('%H:%M:%S')
    
    timestamp_log.append(current_time)
    memory_usage_log.append(used_percentage)
    
    print(f"📦 [{current_node}] Frame {frame+1}/5 captured -> Memory Load: {used_percentage:.2f}%")
    time.sleep(2)

# Stream resource metrics into a Pandas DataFrame structure
data_frame = pd.DataFrame({
    'Time': timestamp_log,
    'Memory Load (%)': memory_usage_log
})

# Compile and style the system tracking diagram
plt.figure(figsize=(8, 4))
sns.lineplot(data=data_frame, x='Time', y='Memory Load (%)', marker='o', color='purple', linewidth=2.5)
plt.title(f'Infrastructure Analytics: Real-Time Resource Trace [{current_node}]', fontsize=12, fontweight='bold')
plt.ylim(0, 100)

# Save the visualization directly to the user home folder
output_image = f'memory_utilization_{current_node}.png'
plt.savefig(output_image, bbox_inches='tight', dpi=150)
print(f"📊 Success! Visualization generated at: {os.path.abspath(output_image)}")
