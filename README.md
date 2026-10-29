# Factory Traffic Management System - CSI Smart Tech Assessment

## Setup and Run Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Create a superuser: `python manage.py createsuperuser`
4. Start the server: `python manage.py runserver`
5. Go to `http://127.0.0.1:8000/admin/` and log in.
6. Create a `Junction` (Name: A) and create `SignalStates` for NORTH, SOUTH, EAST, WEST.
7. View the dashboard at `http://127.0.0.1:8000/dashboard/`

## Traffic-Control Algorithm Explanation
The system uses a priority-based scheduling algorithm combined with a strict safe-state machine. 
- **Starvation Prevention:** The engine evaluates queue lengths and waiting times to ensure lower-priority vehicles are not blocked indefinitely.
- **State Machine:** It strictly enforces `GREEN -> YELLOW -> ALL RED -> GREEN` transitions.
- **Emergency Handling:** Emergency vehicles trigger a safe preemption. Conflicting phases are never GREEN simultaneously.

## Assumptions / Questions / Requirement Issues
- **Time Constraint:** Due to a limited timeframe (approx. 1 hour), the core domain logic, safe transitions, and API endpoints were prioritized over frontend polish and advanced concurrency locking.
- **Manual Mode:** Manual mode remains active until the admin sends `RETURN_TO_AUTOMATIC`. It does not auto-expire in this version.
- **Controller ACK:** Since physical controllers are not available, actual states are simulated via the API.
- **Concurrency:** To prevent race conditions in this limited timeframe, the system processes events sequentially. 
- **Duplicate Events:** Handled strictly by using `event_id` as a unique key in the `ProcessedEvent` model.

## AI / Tool Usage
AI-assisted tools (like ChatGPT/DeepSeek) were used for:
- Generating boilerplate Django models, serializers, and views.
- Structuring the state machine logic.
- Drafting this README documentation.
All code and logic have been reviewed and can be explained during the technical review.

## Major Architectural Decisions
- **Separation of Concerns:** The core traffic logic is isolated in `traffic_engine.py` and does not depend on HTTP or the database schema.
- **Background Thread:** A background thread is used to manage automatic signal timing without blocking API request handlers (avoiding `time.sleep()` in views).