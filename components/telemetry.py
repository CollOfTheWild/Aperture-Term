from datetime import datetime
import psutil
from textual.app import ComposeResult
from textual.widgets import Static
from textual.reactive import reactive

try:
    import pynvml
    HAS_NVIDIA = True
except ImportError:
    HAS_NVIDIA = False

class Telemetry(Static):
    """
    [Bot-Right] Hardware Vitals
    GPU/CPU/RAM monitoring.
    """
    BORDER_TITLE = "TELEMETRY [4]"
    
    # Reactive strings to update the UI efficiently
    cpu_str = reactive("CPU:  ---%")
    ram_str = reactive("RAM:  ---%")
    gpu_str = reactive("GPU:  ---")
    
    def on_mount(self) -> None:
        """Initialize monitoring."""
        global HAS_NVIDIA
        if HAS_NVIDIA:
            try:
                pynvml.nvmlInit()
            except Exception:
                # Fallback if drivers are missing or init fails
                HAS_NVIDIA = False
        
        # Update every 1 second (1Hz)
        self.set_interval(1.0, self.update_stats)

    def update_stats(self) -> None:
        """Fetch and update hardware stats."""
        # CPU & RAM
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        
        self.cpu_str = f"CPU: {cpu_percent:5.1f}%"
        self.ram_str = f"RAM: {ram.percent:5.1f}% ({ram.used / (1024**3):.1f}/{ram.total / (1024**3):.1f} GB)"

        # GPU
        if HAS_NVIDIA:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                
                vram_used = mem.used / (1024**2) # MB
                vram_total = mem.total / (1024**2) # MB
                vram_percent = (vram_used / vram_total) * 100
                
                self.gpu_str = (
                    f"GPU: {vram_percent:5.1f}% | "
                    f"MEM: {vram_used:.0f}/{vram_total:.0f} MB | "
                    f"TMP: {temp}°C"
                )
            except Exception as e:
                self.gpu_str = f"GPU: ERR ({str(e)})"
        else:
            self.gpu_str = "GPU: N/A"

    def compose(self) -> ComposeResult:
        # We wrap reactives in Static widgets or labels
        # Here we just re-render the whole content or separate lines
        yield Static(id="telemetry_cpu")
        yield Static(id="telemetry_ram")
        yield Static(id="telemetry_gpu")

    def watch_cpu_str(self, new_val: str) -> None:
        self.query_one("#telemetry_cpu", Static).update(new_val)

    def watch_ram_str(self, new_val: str) -> None:
        self.query_one("#telemetry_ram", Static).update(new_val)
        
    def watch_gpu_str(self, new_val: str) -> None:
        self.query_one("#telemetry_gpu", Static).update(new_val)