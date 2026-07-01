from fastapi import HTTPException

from app.models.plan import Plan


class PlanService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_plan(
        db,
        plan_id,
    ):

        plan = (
            db.query(Plan)
            .filter(
                Plan.plan_id == plan_id
            )
            .first()
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan not found.",
            )

        return plan

    @staticmethod
    def _validate_plan_name(
        db,
        plan_name,
        exclude_plan_id=None,
    ):

        query = (
            db.query(Plan)
            .filter(
                Plan.plan_name == plan_name
            )
        )

        if exclude_plan_id is not None:

            query = query.filter(
                Plan.plan_id != exclude_plan_id
            )

        existing_plan = query.first()

        if existing_plan:

            raise HTTPException(
                status_code=400,
                detail="A plan with this name already exists.",
            )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_plan(
        db,
        plan_data,
    ):

        PlanService._validate_plan_name(
            db,
            plan_data.plan_name,
        )

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
    def update_plan_details(
        db,
        plan_id,
        plan_data,
    ):

        plan = (
            PlanService._find_plan(
                db,
                plan_id,
            )
        )

        PlanService._validate_plan_name(
            db,
            plan_data.plan_name,
            exclude_plan_id=plan_id,
        )

        plan.plan_name = plan_data.plan_name
        plan.price = plan_data.price
        plan.duration_days = plan_data.duration_days
        plan.speed_limit_mbps = (
            plan_data.speed_limit_mbps
        )
        plan.max_devices = (
            plan_data.max_devices
        )
        plan.concurrent_devices = (
            plan_data.concurrent_devices
        )

        db.commit()

        db.refresh(plan)

        return plan

    @staticmethod
    def activate_plan(
        db,
        plan_id,
    ):

        plan = (
            PlanService._find_plan(
                db,
                plan_id,
            )
        )

        plan.is_active = True

        db.commit()

        db.refresh(plan)

        return plan

    @staticmethod
    def deactivate_plan(
        db,
        plan_id,
    ):

        plan = (
            PlanService._find_plan(
                db,
                plan_id,
            )
        )

        plan.is_active = False

        db.commit()

        db.refresh(plan)

        return plan

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_plan(
        db,
        plan_id,
    ):

        return (
            PlanService._find_plan(
                db,
                plan_id,
            )
        )

    @staticmethod
    def get_active_plans(
        db,
    ):

        return (
            db.query(Plan)
            .filter(
                Plan.is_active.is_(True)
            )
            .order_by(
                Plan.price
            )
            .all()
        )

    @staticmethod
    def get_all_plans(
        db,
    ):

        return (
            db.query(Plan)
            .order_by(
                Plan.price
            )
            .all()
        )