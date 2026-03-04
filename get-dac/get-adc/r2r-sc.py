import time
from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time

def main():
    # Параметры эксперимента
    MY_DYNAMIC_RANGE = 3.3
    duration = 3.0
    voltage_values = []
    time_values = []
    
    adc = None
    try:
        # Инициализация с быстрым временем сравнения
        adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, compare_time=0.0001)
        
        start_time = time.time()
        print(f"Запись данных в течение {duration} сек...")

        while (time.time() - start_time) < duration:
            current_elapsed = time.time() - start_time
            
            # Измеряем напряжение и фиксируем время
            v = adc.get_sc_voltage()
            
            voltage_values.append(v)
            time_values.append(current_elapsed)

        print("Запись завершена. Построение графика...")
        plot_voltage_vs_time(time_values, voltage_values, MY_DYNAMIC_RANGE)

    except KeyboardInterrupt:
        print("\nПрервано пользователем")
    finally:
        if adc:
            del adc

if __name__ == "__main__":
    main()
