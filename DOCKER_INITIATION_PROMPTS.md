**View logs:**

&nbsp; docker compose logs -f



&nbsp; Stop all services:

&nbsp; docker compose down



**Restart services:**

&nbsp; docker compose restart



**Initialize DB:**

&nbsp; docker compose exec backend python -m app.utils.init\_db

&nbsp;



**Recreate Database (Will lose existing data):**

&nbsp; docker compose down -v

&nbsp; docker compose up -d

&nbsp; docker compose exec backend python -m app.utils.init\_db





