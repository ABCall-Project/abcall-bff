DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'abcall-db'
   ) THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE "abcall-db"');
   END IF;
END
$do$;



CREATE TABLE IF NOT EXISTS issue_state(
   id UUID PRIMARY KEY,
   name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS issue(
   id UUID PRIMARY KEY,
   auth_user_id UUID,
   auth_user_agent_id UUID,
   status UUID,
   subject VARCHAR(255),
   description TEXT,
   created_at TIMESTAMP WITH TIME ZONE,
   closed_at TIMESTAMP WITH TIME ZONE,
   channel_plan_id UUID,
   CONSTRAINT fk_status
        FOREIGN KEY (status) 
        REFERENCES issue_state (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS issue_attachment (
    id UUID PRIMARY KEY,
    file_path VARCHAR(255),
    issue_id UUID,
    CONSTRAINT fk_issue
        FOREIGN KEY (issue_id) 
        REFERENCES issue (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS role(
   id UUID PRIMARY KEY,
   name VARCHAR(20)
);


CREATE TABLE IF NOT EXISTS auth_user (
    id UUID PRIMARY KEY,
    name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(10),
    email VARCHAR(100),
    address VARCHAR(255),
    birthdate TIMESTAMP WITH TIME ZONE,
    password VARCHAR(255),
    role_id UUID,
    salt VARCHAR(255),
    CONSTRAINT fk_role
        FOREIGN KEY (role_id) 
        REFERENCES role (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS auth_user_customer(
   id UUID PRIMARY KEY,
   auth_user_id UUID,
   customer_id UUID,
   CONSTRAINT fk_user
        FOREIGN KEY (auth_user_id) 
        REFERENCES auth_user (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS channel(
   id UUID PRIMARY KEY,
   name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS plan(
   id UUID PRIMARY KEY,
   name VARCHAR(20),
   basic_monthly_rate NUMERIC(10, 2),
   issue_fee NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS customer (
    id UUID PRIMARY KEY,
    document VARCHAR(20),
    name VARCHAR(150),
    plan_id UUID,
    date_suscription TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_plan
        FOREIGN KEY (plan_id) 
        REFERENCES plan (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS channel_plan (
    id UUID PRIMARY KEY,
    channel_id UUID,
    plan_id UUID,
    CONSTRAINT fk_plan
        FOREIGN KEY (plan_id) 
        REFERENCES plan (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_channel
      FOREIGN KEY (channel_id) 
      REFERENCES channel (id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS customer_database (
    id UUID PRIMARY KEY,
    customer_id UUID,
    topic TEXT,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id) 
        REFERENCES customer (id)
        ON DELETE CASCADE
);