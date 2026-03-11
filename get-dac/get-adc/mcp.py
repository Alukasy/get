import time
import matplotlib.pyplot as plt
from mcp3021_driver import MCP3021

def task_plot():
    DYNAMIC_RANGE = 5.2
    DURATION = 5        
    
    adc = MCP3021(dynamic_range=DYNAMIC_RANGE)
    
    voltages = []
    times = []
    durations = [] 
    
    print(f"Запуск измерений на {DURATION} секунд...")
    
    try:
        start_time = time.time()
        prev_time = start_time
        
        while (time.time() - start_time) < DURATION:
            curr_time = time.time()
            
            v = adc.get_voltage()
            
            voltages.append(v)
            times.append(curr_time - start_time)
            
            step_duration = curr_time - prev_time
            durations.append(step_duration)
            
            prev_time = curr_time
            
            
        print("Сбор данных завершен. Отрисовка...")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        plt.subplots_adjust(hspace=0.3)
        ax1.plot(times, voltages, color='tab:blue', linewidth=0.5)
        ax1.set_title("Зависимость напряжения от времени")
        ax1.set_xlabel("Время, с")
        ax1.set_ylabel("Напряжение, В")
        ax1.grid(True)
        ax1.set_ylim(0, DYNAMIC_RANGE + 0.2)

        ax2.hist(durations, bins=100, color='tab:blue', range=(0, 0.06))
        ax2.set_title("Распределение периодов дискретизации измерений\nпо времени на одно измерение")
        ax2.set_xlabel("Период измерения, с")
        ax2.set_ylabel("Количество измерений")
        ax2.grid(True)
        ax2.set_xlim(0, 0.06)

        plt.show()

    except KeyboardInterrupt:
        print("\nПрервано.")
    finally:
        adc.deinit()

if __name__ == "__main__":
    task_plot()
