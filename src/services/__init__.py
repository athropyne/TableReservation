import src.services.tables
import src.services.reservations

subscribes = [
    *tables.subscribes,
    *reservations.subscribes
]
