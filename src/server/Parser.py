from src.model_checker import State, Event


def function_wrapper(code, variables):
    def __closure():
        exec(code, {'variable': variables})

    if code:
        return __closure
    return None


def parse_state(state: dict, variables: dict) -> State:
    name = state.get("name", None)

    on_enter_state = state.get("on_enter_state", None)
    on_leave_state = state.get("on_leave_state", None)
    if on_enter_state:
        on_enter_state = function_wrapper(on_enter_state, variables)

    if on_leave_state:
        on_leave_state = function_wrapper(on_leave_state, variables)

    initial = state.get('is_initial', False)
    final = state.get('is_finial', False)
    return State(name, on_enter_state, on_leave_state, is_initial=initial, is_final=final)


def parse_event(event: dict, variables: dict) -> Event:
    name = event.get('name', None)
    src = event.get('src', None)
    des = event.get('des', None)
    on_event = event.get("on_event", None)
    if on_event:
        on_event = function_wrapper(on_event, variables)

    return Event(name, src, des, on_event, variables)


def parse_validator(code: str, variable: dict):
    return function_wrapper(code, variable)
