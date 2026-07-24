from app.services.plan_service import (
    PlanService,
)


class RouterProfileService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def profile_from_plan(
        plan,
    ):

        return {

            "name": (

                RouterProfileService

                .profile_name(

                    plan,

                )

            ),

            "plan": plan,

        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_profiles(
        db,
    ):

        plans = (

            PlanService

            .get_all_plans(

                db,

            )["items"]

        )

        profiles = []

        for plan in plans:

            profiles.append(

                {

                    "name": (

                        RouterProfileService

                        .profile_name(

                            plan,

                        )

                    ),

                    "plan": plan,

                }

            )

        return profiles

    @staticmethod
    def profile_name(
        plan,
    ):

        return (

            f"BN-PLAN-"

            f"{plan.plan_id}"

        )