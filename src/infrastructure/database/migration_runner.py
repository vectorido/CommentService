import asyncio
import asyncpg
from pathlib import Path
from src.infrastructure.config import settings


class MigrationRunner:
    def __init__(self, migrations_dir: str = "src/infrastructure/database/migrations"):
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(parents=True, exist_ok=True)
    
    async def _ensure_migrations_table(self, conn):
        await conn.execute("""
            create table if not exists schema_migrations (
                version varchar(255) primary key,
                applied_at timestamp default current_timestamp
            )
        """)
    
    async def _get_applied_migrations(self, conn):
        rows = await conn.fetch("select version from schema_migrations order by version")
        return {row['version'] for row in rows}
    
    async def _get_pending_migrations(self, conn):
        applied = await self._get_applied_migrations(conn)
        all_migrations = sorted([
            f.stem for f in self.migrations_dir.glob("*.sql")
        ])
        return [m for m in all_migrations if m not in applied]
    
    async def migrate(self):
        conn = await asyncpg.connect(
            host=settings.database_host,
            port=settings.database_port,
            database=settings.database_name,
            user=settings.database_user,
            password=settings.database_password,
        )
        
        try:
            await self._ensure_migrations_table(conn)
            pending = await self._get_pending_migrations(conn)
            
            if not pending:
                print("No pending migrations")
                return
            
            for migration_name in pending:
                print(f"Applying migration: {migration_name}")
                
                migration_file = self.migrations_dir / f"{migration_name}.sql"
                sql = migration_file.read_text()
                
                async with conn.transaction():
                    await conn.execute(sql)
                    await conn.execute(
                        "insert into schema_migrations (version) values ($1)",
                        migration_name
                    )
                
                print(f"✅ Applied: {migration_name}")
            
            print(f"\n✅ Successfully applied {len(pending)} migration(s)")
        
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise
        finally:
            await conn.close()
    
    async def status(self):
        conn = await asyncpg.connect(
            host=settings.database_host,
            port=settings.database_port,
            database=settings.database_name,
            user=settings.database_user,
            password=settings.database_password,
        )
        
        try:
            await self._ensure_migrations_table(conn)
            applied = await self._get_applied_migrations(conn)
            all_migrations = sorted([
                f.stem for f in self.migrations_dir.glob("*.sql")
            ])
            
            if not all_migrations:
                print("\n⚠️  No migration files found")
                print(f"Create SQL files in: {self.migrations_dir}")
                return
            
            print("\nMigration Status:")
            print("-" * 70)
            for migration in all_migrations:
                status = "✅ Applied" if migration in applied else "⏳ Pending"
                print(f"{migration:<55} {status}")
            print("-" * 70)
            
            pending_count = len([m for m in all_migrations if m not in applied])
            print(f"\nTotal: {len(all_migrations)} | Applied: {len(applied)} | Pending: {pending_count}")
        
        finally:
            await conn.close()


async def main():
    import sys
    runner = MigrationRunner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        await runner.status()
    else:
        await runner.migrate()


if __name__ == "__main__":
    asyncio.run(main())

