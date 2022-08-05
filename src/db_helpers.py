from sqlmodel import SQLModel

def create_db_and_tables(engine) -> None:
    SQLModel.metadata.create_all(engine)

async def add_items_to_db(items,session) -> bool:
    for item in items:
        session.add(item)
    session.commit()
    return True