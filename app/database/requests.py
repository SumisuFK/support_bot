import asyncpg

async def create_pool(dsn):
    return await asyncpg.create_pool(
        dsn=dsn,
        min_size=1,
        max_size=10
    )

async def close_pool(pool):
    await pool.close()

async def create_ticket(pool, user_id, username, full_name, text):
    async with pool.acquire() as conn:
        ticket_id = await conn.fetchval(
            """
            INSERT INTO support_tickets (user_id, username, full_name, user_message)
            VALUES ($1, $2, $3, $4)
            RETURNING id
            """,
            user_id,
            username,
            full_name,
            text
        )
        return int(ticket_id)

async def get_ticket(pool, ticket_id):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM support_tickets WHERE id = $1",
            ticket_id
        )
        return dict(row) if row else None
