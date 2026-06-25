from app.models.plan import Plan


class PlanService:

    @staticmethod
    def get_all_plans(db):

        return (
            db.query(Plan)
            .filter(Plan.is_active == True)
            .all()
        )