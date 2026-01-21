CREATE TABLE IF NOT EXISTS support_tickets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username TEXT,
    full_name TEXT,
    user_message TEXT,
    root_message_id BIGINT,
    status TEXT NOT NULL DEFAULT 'open'
);

CREATE INDEX IF NOT EXISTS idx_support_tickets_user_id ON support_tickets(user_id);

CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON support_tickets(status);
