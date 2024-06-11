```bash
docker compose up -d
```

```bash
docker run --rm --network="social-network" -v .\social_network_api\migrations:/app liquibase/liquibase:4.19.0 --defaultsFile=/app/dev.properties update
```