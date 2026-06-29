import Chip from "@mui/material/Chip";

const STATUS_COLORS = {

    active: "success",

    inactive: "default",

    suspended: "warning",

    blocked: "error",

    queued: "info",

    expired: "default",

    cancelled: "default",

    successful: "success",

    pending: "warning",

    failed: "error",

    refunded: "info",

};

function BadgeChip({

    label,

    status,

    color,

    size = "small",

    variant = "filled",

}) {

    const chipLabel = label ?? status ?? "-";

    const chipColor =
        color ||
        STATUS_COLORS[status] ||
        "default";

    return (

        <Chip

            label={chipLabel}

            color={chipColor}

            size={size}

            variant={variant}

            sx={{

                fontWeight: 600,

                textTransform: "capitalize",

            }}

        />

    );

}

export default BadgeChip;