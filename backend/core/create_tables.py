from backend.core.database import engine, metadata
from backend.core.models import cure_mediche  # importa la tabella

metadata.create_all(engine)

print("Tabelle create correttamente!")
