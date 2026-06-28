import Chip from "@mui/material/Chip";

const registrationStepConfig = {
    START: {
        label: "Started",
        color: "info",
    },

    NAME: {
        label: "Awaiting Name",
        color: "warning",
    },

    PHONE: {
        label: "Awaiting Phone",
        color: "warning",
    },

    COMPLETE: {
        label: "Complete",
        color: "success",
    },
};

const statusConfig = {
    ACTIVE: {
        label: "Active",
        color: "success",
    },

    INACTIVE: {
        label: "Inactive",
        color: "default",
    },

    REGISTERED: {
        label: "Registered",
        color: "success",
    },

    PENDING: {
        label: "Pending",
        color: "warning",
    },

    SUSPENDED: {
        label: "Suspended",
        color: "error",
    },

    EXPIRED: {
        label: "Expired",
        color: "error",
    },

    ONLINE: {
        label: "Online",
        color: "success",
    },

    OFFLINE: {
        label: "Offline",
        color: "default",
    },
};

function BadgeChip({
    label,
    color = "default",
    variant,
    value,
}) {
    if (variant === "registrationStep") {
        const config = registrationStepConfig[value] || {
            label: value,
            color: "default",
        };

        return (
            <Chip
                label={config.label}
                color={config.color}
                size="small"
            />
        );
    }

    if (variant === "status") {
        const config = statusConfig[value] || {
            label: value,
            color: "default",
        };

        return (
            <Chip
                label={config.label}
                color={config.color}
                size="small"
            />
        );
    }

    return (
        <Chip
            label={label}
            color={color}
            size="small"
        />
    );
}

export default BadgeChip;