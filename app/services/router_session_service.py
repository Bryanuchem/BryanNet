from datetime import (
    datetime,
    UTC,
)

from fastapi import (
    HTTPException,
)

from app.models.router_session import (
    RouterSession,
)

from app.services.device_service import (
    DeviceService,
)

class RouterSessionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================
   
    @staticmethod
    def _find_session(
        db,
        router_session_id,
    ):

        session = (

            db.query(
                RouterSession,
            )

            .filter(

                RouterSession.router_session_id
                == router_session_id,

            )

            .first()

        )

        if not session:

            raise HTTPException(

                status_code=404,

                detail="Session not found.",

            )

        return session

    @staticmethod
    def _find_active_session(
        db,
        router_account_id,
        mac_address=None,
    ):

        query = (

            db.query(
                RouterSession,
            )

            .filter(

                RouterSession.router_account_id
                == router_account_id,

                RouterSession.is_active.is_(True),

            )

        )

        if mac_address:

            query = query.filter(

                RouterSession.mac_address
                == mac_address,

            )

        return query.first()

    @staticmethod
    def _count_active_sessions(
        db,
        router_account_id,
    ):

        return (

            db.query(
                RouterSession,
            )

            .filter(

                RouterSession.router_account_id
                == router_account_id,

                RouterSession.is_active.is_(True),

            )

            .count()

        )

    @staticmethod
    def _find_active_session_by_username(
        db,
        username,
    ):

        return (

            db.query(
                RouterSession,
            )

            .filter(

                RouterSession.username
                == username,

                RouterSession.is_active.is_(True),

            )

            .first()

        )

    @staticmethod
    def _find_active_sessions_by_router(
        db,
        router_id,
    ):

        return (

            db.query(

                RouterSession,

            )

            .filter(

                RouterSession.router_id
                == router_id,

                RouterSession.is_active.is_(True),

            )

            .all()

        )

    @staticmethod
    def _set_active(
        session,
    ):

        session.is_active = True

        session.logout_at = None

        session.updated_at = datetime.now(

            UTC,

        )

    @staticmethod
    def _set_inactive(
        session,
    ):

        session.is_active = False

        session.logout_at = datetime.now(

            UTC,

        )

        session.updated_at = datetime.now(

            UTC,

        )
        
    @staticmethod
    def _create_from_pending_login(
        db,
        *,
        pending_login,
    ):

        existing = RouterSessionService._find_active_session(

            db,

            pending_login.router_account_id,

            pending_login.device_mac,

        )

        if existing:

            return existing

        session = RouterSession(

            pending_login_id=(
                pending_login.pending_login_id
            ),

            router_account_id=(
                pending_login.router_account_id
            ),

            router_id=(
                pending_login.router_id
            ),

            device_id=(
                pending_login.device_id
            ),

            username=(
                pending_login.router_account.username
            ),

            session_type="hotspot",

            ip_address=(
                pending_login.device_ip
            ),

            mac_address=(
                pending_login.device_mac
            ),

            login_source="portal",

            login_at=datetime.now(
                UTC,
            ),

            is_active=True,

        )

        db.add(
            session,
        )

        db.flush()

        return session

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_session(
        db,
        *,
        router_account_id,
        router_id,
        username,
        session_type,
        ip_address=None,
        mac_address=None,
        login_source=None,
        device_id=None,
    ):

        print("=== CREATE SESSION ===")
        print("mac_address:", repr(mac_address))
        print("device_id:", device_id)

        existing = (

            RouterSessionService
            ._find_active_session(

                db,

                router_account_id,

                mac_address,

            )

        )

        if existing:

            existing.ip_address = (
                ip_address
            )

            existing.mac_address = (
                mac_address
            )

            existing.device_id = (
                device_id
            )

            existing.login_source = (
                login_source
            )

            #
            # Refresh the most recent
            # successful login time.
            #

            existing.login_at = (
                datetime.now(
                    UTC,
                )
            )

            db.commit()

            db.refresh(
                existing,
            )

            
            print("set_online:", repr(mac_address)) 
            
            if mac_address:

                print(

                    "Calling DeviceService.set_online()",

                )

                DeviceService.set_online(

                    db,

                    mac_address,

                )
                
            return existing
        
        session = RouterSession(

            router_account_id=router_account_id,

            router_id=router_id,

            device_id=device_id,
            
            username=username,

            session_type=session_type,

            ip_address=ip_address,

            mac_address=mac_address,

            login_source=login_source,

            login_at=datetime.now(
                UTC,
            ),

            is_active=True,
        
        )



        db.add(
            session,
        )

        db.commit()

        db.refresh(
            session,
        )

        if mac_address:

            print("Calling DeviceService.set_online()")
            
            DeviceService.set_online(

                db,

                mac_address,

            )

        return session

    @staticmethod
    def update_runtime(
        db,
        *,
        router_session,
        payload,
    ):

        #
        # RouterEventCreate only supplies a subset of
        # runtime fields. Update only those fields that
        # actually exist on the payload.
        #

        if getattr(payload, "ip_address", None) is not None:

            router_session.ip_address = (
                payload.ip_address
            )

        if getattr(payload, "mac_address", None) is not None:

            router_session.mac_address = (
                payload.mac_address
            )

        #
        # Logout statistics.
        #

        if hasattr(payload, "bytes_in"):

            router_session.bytes_in = (
                payload.bytes_in or 0
            )

        if hasattr(payload, "bytes_out"):

            router_session.bytes_out = (
                payload.bytes_out or 0
            )

        if hasattr(payload, "packets_in"):

            router_session.packets_in = (
                payload.packets_in or 0
            )

        if hasattr(payload, "packets_out"):

            router_session.packets_out = (
                payload.packets_out or 0
            )

        if hasattr(payload, "disconnect_reason"):

            router_session.disconnect_reason = (
                payload.disconnect_reason
            )

        db.commit()

        db.refresh(
            router_session,
        )

        return router_session

    @staticmethod
    def close_session(
        db,
        *,
        router_account_id,
        mac_address=None,
        bytes_in=0,
        bytes_out=0,
        packets_in=0,
        packets_out=0,
        disconnect_reason=None,
    ):

        session = (

            RouterSessionService
            ._find_active_session(

                db,

                router_account_id,

                mac_address,

            )

        )

        if not session:

            raise HTTPException(

                status_code=404,

                detail=(
                    "Active session not found."
                ),

            )

        session.logout_at = (

            datetime.now(
                UTC,
            )

        )

        session.is_active = False

        session.bytes_in = (
            bytes_in
        )

        session.bytes_out = (
            bytes_out
        )

        session.packets_in = (
            packets_in
        )

        session.packets_out = (
            packets_out
        )

        session.disconnect_reason = (
            disconnect_reason
        )

        db.commit()

        db.refresh(
            session,
        )

        if session.mac_address:

            DeviceService.set_offline(

                db,

                session.mac_address,

            )

        return session

    @staticmethod
    def close_all_sessions(
        db,
        *,
        router_account_id,
        disconnect_reason=None,
    ):

        sessions = (

            db.query(
                RouterSession,
            )

            .filter(

                RouterSession.router_account_id
                == router_account_id,

                RouterSession.is_active.is_(True),

            )

            .all()

        )

        now = datetime.now(
            UTC,
        )

        for session in sessions:

            session.logout_at = now

            session.is_active = False

            session.disconnect_reason = (
                disconnect_reason
            )

            if session.mac_address:

                DeviceService.set_offline(

                    db,

                    session.mac_address,

                )
                
        db.commit()

        return sessions

    @staticmethod
    def synchronize_runtime(
        db,
        *,
        router_id,
        hotspot_sessions,
        ppp_sessions,
    ):

        hotspot_usernames = {

            session.get(
                "user",
            )

            for session in hotspot_sessions

            if session.get(
                "user",
            )

        }

        ppp_usernames = {

            session.get(
                "username",
            )

            for session in ppp_sessions

            if session.get(
                "username",
            )

        }

        active_usernames = (

            hotspot_usernames

            |

            ppp_usernames

        )

        sessions = (

            db.query(
                RouterSession,
            )

            .filter(

                RouterSession.router_id
                == router_id,

            )

            .all()

        )

        activated = 0

        deactivated = 0

        unchanged = 0

        for session in sessions:

            should_be_active = (

                session.username

                in

                active_usernames

            )

            if should_be_active:

                if not session.is_active:

                    RouterSessionService._set_active(

                        session,

                    )

                    activated += 1

                else:

                    unchanged += 1

                if session.mac_address:

                    DeviceService.set_online(

                        db,

                        session.mac_address,

                    )

            else:

                if session.is_active:

                    RouterSessionService._set_inactive(

                        session,

                    )

                    deactivated += 1

                else:

                    unchanged += 1

                if session.mac_address:

                    DeviceService.set_offline(

                        db,

                        session.mac_address,

                    )

        db.commit()

        return {

            "success": True,

            "activated": activated,

            "deactivated": deactivated,

            "unchanged": unchanged,

            "total": len(

                sessions,

            ),

        }
        
    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_active_session(
        db,
        *,
        router_account_id,
        mac_address=None,
    ):

        return (

            RouterSessionService
            ._find_active_session(

                db,

                router_account_id,

                mac_address,

            )

        )

    @staticmethod
    def get_active_session_by_username(
        db,
        *,
        username,
    ):

        return (

            RouterSessionService

            ._find_active_session_by_username(

                db,

                username,

            )

        )

    @staticmethod
    def count_active_sessions(
        db,
        *,
        router_account_id,
    ):

        return (

            RouterSessionService
            ._count_active_sessions(

                db,

                router_account_id,

            )

        )

    @staticmethod
    def is_customer_online(
        db,
        *,
        router_account_id,
    ):

        return (

            RouterSessionService

            .count_active_sessions(

                db,

                router_account_id=router_account_id,

            )

            > 0

        )

    @staticmethod
    def get_customer_sessions(
        db,
        *,
        router_account_id,
    ):

        return (

            db.query(
                RouterSession,
            )

            .filter(

                RouterSession.router_account_id
                == router_account_id,

            )

            .order_by(

                RouterSession.login_at.desc(),

            )

            .all()

        )