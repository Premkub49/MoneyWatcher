use std::env;
mod db;
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenvy::dotenv().ok();
    let database_url =
        env::var("DB_URL").map_err(|e| format!("Not Found DB_URL in .env: {}", e))?;

    let pool = db::establish_connection(&database_url).await?;

    #[derive(sqlx::FromRow)]
    struct DbName {
        datname: String,
    }

    let databases = sqlx::query_as::<_, DbName>(
        "SELECT datname FROM pg_database WHERE datistemplate = false AND datname != 'postgres'",
    )
    .fetch_all(&pool)
    .await?;

    let db_names: Vec<String> = databases.into_iter().map(|db| db.datname).collect();

    println!("{:?}", db_names);
    Ok(())
}
