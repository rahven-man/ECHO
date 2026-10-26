USE echo_staging;

DROP TABLE IF EXISTS business;

CREATE TABLE business (
    business_id   CHAR(22)      NOT NULL,
    name          VARCHAR(255)  NOT NULL,
    address       VARCHAR(255)  NULL,
    city          VARCHAR(100)  NULL,
    state         VARCHAR(10)   NULL,
    postal_code   VARCHAR(20)   NULL,
    latitude      DOUBLE        NULL,
    longitude     DOUBLE        NULL,
    stars         DECIMAL(2,1)  NULL,
    review_count  INT           NULL,
    is_open       TINYINT       NULL,
    attributes    JSON          NULL,
    categories    VARCHAR(1000) NULL,
    hours         JSON          NULL,
    PRIMARY KEY (business_id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;