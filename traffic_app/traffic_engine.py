import time
import threading
from .models import Junction, SignalState

def safe_transition(junction, next_phase):
    states = SignalState.objects.filter(junction=junction)
    current_directions = ['NORTH', 'SOUTH'] if junction.current_phase == 'NORTH_SOUTH' else ['EAST', 'WEST']
    next_directions = ['NORTH', 'SOUTH'] if next_phase == 'NORTH_SOUTH' else ['EAST', 'WEST']
    
    for d in current_directions:
        states.filter(direction=d).update(desired_state='YELLOW')
    time.sleep(5)
    
    states.update(desired_state='RED')
    time.sleep(2)
    
    for d in next_directions:
        states.filter(direction=d).update(desired_state='GREEN')
    
    junction.current_phase = next_phase
    junction.save()

def automatic_loop():
    while True:
        try:
            junction = Junction.objects.first()
            if junction and junction.mode == 'AUTOMATIC':
                next_phase = 'EAST_WEST' if junction.current_phase == 'NORTH_SOUTH' else 'NORTH_SOUTH'
                safe_transition(junction, next_phase)
            time.sleep(30)
        except Exception:
            time.sleep(5)

def start_engine():
    thread = threading.Thread(target=automatic_loop)
    thread.daemon = True
    thread.start()