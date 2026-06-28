from fastapi import HTTPException

from app.models.plan import Plan


class PlanService:

    @staticmethod
    def get_all_plans(db):
        return db.query(Plan).all()

    @staticmethod
    def create_plan(db, plan_data):
        plan = Plan(
            plan_name=plan_data.plan_name,
            price=plan_data.price,
            duration_days=plan_data.duration_days,
            speed_limit_mbps=plan_data.speed_limit_mbps,
            max_devices=plan_data.max_devices,
            concurrent_devices=plan_data.concurrent_devices,
            is_active=plan_data.is_active,
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return plan

    @staticmethod
    def update_plan(db, plan_id, plan):
        existing_plan = (
            db.query(Plan)
            .filter(Plan.plan_id == plan_id)
            .first()
        )

        if not existing_plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found.",
            )

        existing_plan.plan_name = plan.plan_name
        existing_plan.price = plan.price
        existing_plan.duration_days = plan.duration_days
        existing_plan.speed_limit_mbps = plan.speed_limit_mbps
        existing_plan.max_devices = plan.max_devices
        existing_plan.concurrent_devices = plan.concurrent_devices
        existing_plan.is_active = plan.is_active

        db.commit()
        db.refresh(existing_plan)

        return existing_plan

    @staticmethod
    def set_plan_status(db, plan_id, is_active):
        plan = (
            db.query(Plan)
            .filter(Plan.plan_id == plan_id)
            .first()
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found.",
            )

        plan.is_active = is_active

        db.commit()
        db.refresh(plan)

        return plan
    
    @staticmethod
    def delete_plan(db, plan_id):
        plan = (
            db.query(Plan)
            .filter(Plan.plan_id == plan_id)
            .first()
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found.",
            )

        db.delete(plan)
        db.commit()

        return {
            "message": "Plan deleted successfully."
        }