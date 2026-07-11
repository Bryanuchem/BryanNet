from fastapi import HTTPException

from typing import cast

from app.services.audit_log_service import AuditLogService

from app.constants.audit_actions import (
    CREATE_PLAN,
    UPDATE_PLAN,
    ACTIVATE_PLAN,
    DEACTIVATE_PLAN,
)

from app.enums.audit_result import AuditResult

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

    @staticmethod
    def _apply_sort(
        query,
        *sort_columns,
        sort_order,
    ):

        columns = [

            column.desc()

            if sort_order.lower() == "desc"

            else column.asc()

            for column in sort_columns

        ]

        return query.order_by(*columns)

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_plan(
        db,
        plan_data,
        admin_id,
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

        db.flush()

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(int, admin_id),

            action=CREATE_PLAN,

            entity_type="Plan",

            entity_id=cast(int, plan.plan_id),

            target_name=cast(str, plan.plan_name),

            result=AuditResult.SUCCESS,

            description=(
                f"Plan '{plan.plan_name}' was created."
            ),

            new_values={
                "price": float(cast(float, plan.price)),
                "duration_days": float(cast(float, plan.duration_days)),
                "speed_limit_mbps": plan.speed_limit_mbps,
                "max_devices": plan.max_devices,
                "concurrent_devices": plan.concurrent_devices,
                "is_active": plan.is_active,
            },

        )

        db.commit()

        db.refresh(plan)

        return plan

    @staticmethod
    def update_plan_details(
        db,
        plan_id,
        plan_data,
        admin_id,
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

        old_values = {
            "plan_name": plan.plan_name,
            "price": float(plan.price),
            "duration_days": float(plan.duration_days),
            "speed_limit_mbps": plan.speed_limit_mbps,
            "max_devices": plan.max_devices,
            "concurrent_devices": plan.concurrent_devices,
            "is_active": plan.is_active,
        }

        plan.plan_name = plan_data.plan_name
        plan.price = plan_data.price
        plan.duration_days = plan_data.duration_days
        plan.speed_limit_mbps = plan_data.speed_limit_mbps
        plan.max_devices = plan_data.max_devices
        plan.concurrent_devices = plan_data.concurrent_devices

        AuditLogService.log_admin_action(
            
            db=db,

            admin_id=cast(int, admin_id),

            action=UPDATE_PLAN,

            entity_type="Plan",

            entity_id=cast(int, plan.plan_id),

            target_name=cast(str, plan.plan_name),

            result=AuditResult.SUCCESS,

            description=(
                f"Plan '{plan.plan_name}' was updated."
            ),

            old_values=old_values,

            new_values={
                "plan_name": plan.plan_name,
                "price": float(plan.price),
                "duration_days": float(plan.duration_days),
                "speed_limit_mbps": plan.speed_limit_mbps,
                "max_devices": plan.max_devices,
                "concurrent_devices": plan.concurrent_devices,
                "is_active": plan.is_active,
            },
        )

        db.commit()

        db.refresh(plan)

        return plan

    @staticmethod
    def activate_plan(
        db,
        plan_id,
        admin_id,
    ):

        plan = (
            PlanService._find_plan(
                db,
                plan_id,
            )
        )

        plan.is_active = True

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(int, admin_id),

            action=ACTIVATE_PLAN,

            entity_type="Plan",

            entity_id=cast(int, plan.plan_id),

            target_name=cast(str, plan.plan_name),

            result=AuditResult.SUCCESS,

            description=(
                f"Plan '{plan.plan_name}' was activated."
            ),

            old_values={

                "is_active": False,

            },

            new_values={

                "is_active": True,

            },

        )

        db.commit()

        db.refresh(plan)

        return plan

    @staticmethod
    def deactivate_plan(
        db,
        plan_id,
        admin_id,
    ):

        plan = (
            PlanService._find_plan(
                db,
                plan_id,
            )
        )

        plan.is_active = False

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(int, admin_id),

            action=DEACTIVATE_PLAN,

            entity_type="Plan",

            entity_id=cast(int, plan.plan_id),

            target_name=cast(str, plan.plan_name),

            result=AuditResult.SUCCESS,

            description=(
                f"Plan '{plan.plan_name}' was deactivated."
            ),

            old_values={

                "is_active": True,

            },

            new_values={

                "is_active": False,

            },

        )

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
        page=1,
        page_size=25,
        search=None,
        is_active=None,
        sort_by="price",
        sort_order="asc",
    ):

        query = db.query(Plan)

        if search:

            query = query.filter(

                Plan.plan_name.ilike(
                    f"%{search}%"
                )

            )

        if is_active is not None:

            query = query.filter(

                Plan.is_active == is_active

            )

        total = query.count()

        sort_column = {

            "plan_name":
                Plan.plan_name,

            "price":
                Plan.price,

            "duration_days":
                Plan.duration_days,

            "speed_limit_mbps":
                Plan.speed_limit_mbps,

            "max_devices":
                Plan.max_devices,

            "concurrent_devices":
                Plan.concurrent_devices,

        }.get(

            sort_by,

            Plan.price,

        )

        query = PlanService._apply_sort(

            query,

            sort_column,

            sort_order=sort_order,

        )

        plans = (

            query

            .offset(
                (page - 1) * page_size,
            )

            .limit(
                page_size,
            )

            .all()

        )

        pages = (

            (total + page_size - 1)

            // page_size

            if total

            else 0

        )

        return {

            "items": plans,

            "total": total,

            "page": page,

            "page_size": page_size,

            "pages": pages,

        }