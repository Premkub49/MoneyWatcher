use sqlx::{Error, Pool, Postgres, postgres::PgPoolOptions};

pub async fn establish_connection(database_url: &str) -> Result<Pool<Postgres>, Error> {
    println!("Connecting to DB...");

    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(database_url)
        .await?;

    println!("Connect Success");
    Ok(pool)
}
