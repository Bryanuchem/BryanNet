from app.database.database import SessionLocal

from app.services.automation_service import (
    AutomationService,
)


class AutomationRunner:

    @staticmethod
    def run():

        db = SessionLocal()

        try:

            return (
                AutomationService.run_all_jobs(
                    db,
                )
            )

        finally:

            db.close()
            
if __name__ == "__main__":

    result = (
        AutomationRunner.run()
    )

    print(result)            