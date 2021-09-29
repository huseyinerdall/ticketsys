APP_NAME = 'TicketSYS'
APP_VERSION = '1.0.0'

TICKET_TYPES = [
    'Epic',
    'Bug',
    'Task',
    'Subtask',
    'Change',
    'IT help',
    'Incident',
    'New feature',
    'Problem',
    'Service request',
    'Support'
]

TICKET_STATUS_TYPES = [
    'Open',
    'In Progress',
    'Done',
    'To Do',
    'In Review',
    'Under review',
    'Approved',
    'Cancelled',
    'Rejected',
    'Draft',
    'Published',
    'Interviewing',
    'Accepted',
    'Purchased',
    'Requested'
]

TICKET_SEVERITY_TYPES = [
    "Extraordinary",
    "High",
    "Moderate",
    "Low"
]

TICKET_TYPE_COLORS = [

]

def get_context(request):
    return {
        'APP_NAME': APP_NAME,
        'APP_VERSION': APP_VERSION,
        'TICKET_TYPES': TICKET_TYPES,
        'TICKET_STATUS_TYPES': TICKET_STATUS_TYPES,
        'TICKET_SEVERITY_TYPES': TICKET_SEVERITY_TYPES,
    }
