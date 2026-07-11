import Chip from "@mui/material/Chip";

const STATUS_COLORS = {

    active: "success",

    inactive: "error",

    suspended: "warning",

    blocked: "error",

    queued: "info",

    expired: "default",

    cancelled: "default",

    successful: "success",

    success: "success",

    pending: "warning",

    failed: "error",

    warning: "warning",

    info: "info",

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