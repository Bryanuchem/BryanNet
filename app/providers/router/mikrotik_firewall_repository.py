from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikFirewallRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _filter_rules(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "firewall",

                "filter",

            )

        )

    @staticmethod
    def _nat_rules(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "firewall",

                "nat",

            )

        )

    @staticmethod
    def _mangle_rules(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "firewall",

                "mangle",

            )

        )

    @staticmethod
    def _raw_rules(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "firewall",

                "raw",

            )

        )

    @staticmethod
    def _to_rule(
        rule,
    ):

        data = {

            "id": rule.get(
                ".id",
            ),

            "chain": rule.get(
                "chain",
            ),

            "action": rule.get(
                "action",
            ),

            "comment": rule.get(
                "comment",
            ),

            "disabled": rule.get(
                "disabled",
            ),

            "dynamic": rule.get(
                "dynamic",
            ),

            "bytes": rule.get(
                "bytes",
            ),

            "packets": rule.get(
                "packets",
            ),

        }

        mappings = {

            "connection-state":
                "connection_state",

            "out-interface":
                "out_interface",

            "src-address":
                "src_address",

            "src-address-list":
                "src_address_list",

            "new-connection-mark":
                "new_connection_mark",

            "passthrough":
                "passthrough",

            "log":
                "log",

            "log-prefix":
                "log_prefix",

        }

        for mikrotik_name, bryannet_name in (

            mappings.items()

        ):

            if mikrotik_name in rule:

                data[

                    bryannet_name

                ] = rule.get(

                    mikrotik_name,

                )

        return data

    @staticmethod
    def _find(
        resource,
        rule_id,
    ):

        for rule in resource:

            if (

                rule.get(

                    ".id",

                )

                == rule_id

            ):

                return rule

        return None

    @staticmethod
    def _get(
        resource,
        rule_id,
    ):

        rule = (

            MikroTikFirewallRepository

            ._find(

                resource,

                rule_id,

            )

        )

        if rule is None:

            raise ValueError(

                f"Firewall rule "

                f"'{rule_id}' "

                "was not found."

            )

        return (

            MikroTikFirewallRepository

            ._to_rule(

                rule,

            )

        )

    @staticmethod
    def _get_all(
        resource,
    ):

        return [

            (

                MikroTikFirewallRepository

                ._to_rule(

                    rule,

                )

            )

            for rule in resource

        ]
  
    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find_nat_by_comment(
        api,
        comment,
    ):

        for rule in (

            MikroTikFirewallRepository

            ._nat_rules(

                api,

            )

        ):

            if (

                rule.get(

                    "comment",

                )

                == comment

            ):

                return (

                    MikroTikFirewallRepository

                    ._to_rule(

                        rule,

                    )

                )

        return None
    
    # ==========================================================
    # Filter Rules
    # ==========================================================

    @staticmethod
    def get_filter_rules(
        api,
    ):

        return (

            MikroTikFirewallRepository

            ._get_all(

                MikroTikFirewallRepository

                ._filter_rules(

                    api,

                )

            )

        )

    @staticmethod
    def get_filter_rule(
        api,
        rule_id,
    ):

        return (

            MikroTikFirewallRepository

            ._get(

                MikroTikFirewallRepository

                ._filter_rules(

                    api,

                ),

                rule_id,

            )

        )

    # ==========================================================
    # NAT Rules
    # ==========================================================

    @staticmethod
    def get_nat_rules(
        api,
    ):

        return (

            MikroTikFirewallRepository

            ._get_all(

                MikroTikFirewallRepository

                ._nat_rules(

                    api,

                )

            )

        )

    @staticmethod
    def get_nat_rule(
        api,
        rule_id,
    ):

        return (

            MikroTikFirewallRepository

            ._get(

                MikroTikFirewallRepository

                ._nat_rules(

                    api,

                ),

                rule_id,

            )

        )
    
    # ==========================================================
    # Mangle Rules
    # ==========================================================

    @staticmethod
    def get_mangle_rules(
        api,
    ):

        return (

            MikroTikFirewallRepository

            ._get_all(

                MikroTikFirewallRepository

                ._mangle_rules(

                    api,

                )

            )

        )

    @staticmethod
    def get_mangle_rule(
        api,
        rule_id,
    ):

        return (

            MikroTikFirewallRepository

            ._get(

                MikroTikFirewallRepository

                ._mangle_rules(

                    api,

                ),

                rule_id,

            )

        )

    # ==========================================================
    # Raw Rules
    # ==========================================================

    @staticmethod
    def get_raw_rules(
        api,
    ):

        return (

            MikroTikFirewallRepository

            ._get_all(

                MikroTikFirewallRepository

                ._raw_rules(

                    api,

                )

            )

        )

    @staticmethod
    def get_raw_rule(
        api,
        rule_id,
    ):

        return (

            MikroTikFirewallRepository

            ._get(

                MikroTikFirewallRepository

                ._raw_rules(

                    api,

                ),

                rule_id,

            )

        )
        
    @staticmethod
    def create_nat(
        api,
        *,
        chain,
        action,
        out_interface,
        comment,
    ):

        (

            MikroTikFirewallRepository

            ._nat_rules(

                api,

            )

            .add(

                chain=chain,

                action=action,

                **{

                    "out-interface": out_interface,

                    "comment": comment,

                },

            )

        )

    @staticmethod
    def rename_nat(
        api,
        rule,
        comment,
    ):

        (

            MikroTikFirewallRepository

            ._nat_rules(

                api,

            )

            .update(

                **{

                    ".id": rule["id"],

                    "comment": comment,

                },

            )

        )
        
    @staticmethod
    def update_nat(
        api,
        rule,
        *,
        chain,
        action,
        out_interface,
        comment,
    ):

        (

            MikroTikFirewallRepository

            ._nat_rules(

                api,

            )

            .update(

                **{

                    ".id": rule["id"],

                    "chain": chain,

                    "action": action,

                    "out-interface": out_interface,

                    "comment": comment,

                },

            )

        )

    @staticmethod
    def delete_nat(
        api,
        rule,
    ):

        (

            MikroTikFirewallRepository

            ._nat_rules(

                api,

            )

            .remove(

                rule["id"],

            )

        )
     
    # ==========================================================
    # Convenience
    # ==========================================================

    @staticmethod
    def ensure_nat(
        api,
        *,
        chain,
        action,
        out_interface,
        comment,
    ):

        rule = (

            MikroTikFirewallRepository

            .find_nat_by_comment(

                api,

                comment,

            )

        )

        if rule is None:

            MikroTikFirewallRepository.create_nat(

                api,

                chain=chain,

                action=action,

                out_interface=out_interface,

                comment=comment,

            )

            return True

        changed = (

            rule.get(

                "chain",

            )

            != chain

            or

            rule.get(

                "action",

            )

            != action

            or

            rule.get(

                "out_interface",

            )

            != out_interface

        )

        if changed:

            MikroTikFirewallRepository.update_nat(

                api,

                rule,

                chain=chain,

                action=action,

                out_interface=out_interface,

                comment=comment,

            )

        return changed
